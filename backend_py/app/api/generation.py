import os
import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from nanoid import generate
from sqlalchemy.orm import Session

from ..auth import get_current_user_id
from ..db import get_db
from .frameworks_shared import (
    GenerateResponse,
    TextGenerateRequest,
    process_with_global_llm,
    process_with_local_llm,
    read_file_content,
    save_framework_to_db,
)


router = APIRouter()


def _extract_keywords(title: str) -> list[str]:
    return [word.strip() for word in title.lower().split() if len(word.strip()) > 3][:5]


def _extract_sections_from_content(file_name: str, content: str) -> list[dict]:
    sections = []
    current_section_lines = []

    for line in content.strip().split("\n")[:50]:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        is_heading = len(line_stripped) < 100 and (
            line_stripped[0].isdigit()
            or line_stripped.isupper()
            or any(
                marker in line_stripped.lower()
                for marker in ["step", "phase", "stage", "chapter"]
            )
        )

        if is_heading:
            if current_section_lines:
                content_preview = " ".join(current_section_lines)[:200]
                sections.append(
                    {
                        "title": f"{file_name}: {current_section_lines[0][:100]}",
                        "content": content_preview,
                        "level": 1,
                        "source_file": file_name,
                    }
                )
            current_section_lines = [line_stripped]
        elif len(current_section_lines) < 3:
            current_section_lines.append(line_stripped)

    if current_section_lines:
        content_preview = " ".join(current_section_lines)[:200]
        sections.append(
            {
                "title": f"{file_name}: {current_section_lines[0][:100]}",
                "content": content_preview,
                "level": 1,
                "source_file": file_name,
            }
        )

    if not sections and content.strip():
        sections.append(
            {
                "title": file_name,
                "content": content[:200] + ("..." if len(content) > 200 else ""),
                "level": 1,
                "source_file": file_name,
            }
        )

    return sections


def build_deterministic_file_metadata(
    file_names: list[str],
    file_contents: list[str],
) -> dict:
    first_content = file_contents[0].strip() if file_contents else ""
    first_lines = first_content.split("\n") if first_content else []
    first_file_name = file_names[0] if file_names else "Uploaded File"

    if len(file_contents) == 1:
        potential_title = (
            first_lines[0][:150].strip()
            if first_lines and len(first_lines[0].strip()) > 10
            else first_file_name
        )
    elif first_lines and len(first_lines[0].strip()) > 10:
        potential_title = first_lines[0][:150].strip()
    else:
        potential_title = f"Framework from {len(file_names)} files"

    simple_keywords = _extract_keywords(potential_title)
    all_sections = []
    for index, content in enumerate(file_contents):
        file_name = file_names[index] if index < len(file_names) else f"File {index+1}"
        all_sections.extend(_extract_sections_from_content(file_name, content))

    if not all_sections:
        all_sections = [
            {
                "title": name,
                "content": "",
                "level": 1,
                "source_file": name,
            }
            for name in file_names
        ]

    return {
        "doc_id": f"doc-{generate(size=12)}",
        "title": potential_title,
        "subject": potential_title,
        "language": "en",
        "bypass_local_llm": True,
        "keywords": simple_keywords,
        "sections": all_sections[:15],
        "facets": {
            "main_topic": {
                "summary": potential_title,
                "items": [
                    {
                        "value": keyword,
                        "evidence": "",
                        "location": "",
                        "confidence": 0.8,
                    }
                    for keyword in simple_keywords
                ],
            },
            "source_files": {
                "summary": f"Content from {len(file_contents)} file(s)",
                "items": [
                    {
                        "value": name,
                        "evidence": "",
                        "location": "",
                        "confidence": 1.0,
                    }
                    for name in file_names
                ],
            },
        },
        "key_values": [
            {"key": "document_title", "value": potential_title},
            {"key": "file_count", "value": str(len(file_contents))},
            {"key": "processing_mode", "value": "direct_file_metadata"},
            {"key": "source_files", "value": ", ".join(file_names[:3])},
        ],
        "tags": simple_keywords,
        "source_count": len(file_contents),
        "source_files": file_names,
        "triples": [],
        "questions": [],
        "risks": [],
        "actions_todo": [],
        "metrics": [],
        "tables": [],
        "figures": [],
        "extra": {
            "processing_mode": "direct_file_metadata",
            "note": "Deterministic metadata extracted without legacy local LLM",
            "file_names": file_names,
            "total_length": sum(len(content) for content in file_contents),
            "truncated": True,
        },
    }


# ============= API Endpoints =============


@router.post("/generate-from-text", response_model=GenerateResponse)
async def generate_from_text(
    request: TextGenerateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    From a text generation framework (login required)

    Call chain: Front-end text → Local LLM → Global LLM → Save to database → Return to framework
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text content is empty")

        if len(request.text) > 50000:
            raise HTTPException(
                status_code=400, detail="Text too long (max 50,000 characters)"
            )

        #  Whether to use Local LLM depends on use_global_llm.
        if not request.use_global_llm:
            #  Lock ON: Privacy Protection Mode
            print(" Step 1: Processing with Local LLM (Privacy Protection)...")
            metadata = process_with_local_llm(request.text, is_file=False)
            print(f" Local LLM completed. Extracted {len(metadata)} metadata fields")

            print(" Step 2: Processing with Global LLM...")
            framework_result = process_with_global_llm(
                metadata=metadata, model=request.model, use_mock=False
            )
            print(" Global LLM completed")
        else:
            #  Lock OFF: Quick Mode
            print(" Processing with Global LLM (Fast Mode - No Local Processing)...")

            #  1. Extract the title (first line or first 150 characters)
            lines = request.text.strip().split("\n")
            potential_title = lines[0][:150].strip() if lines else "User Content"

            #  2. Simple keyword extraction (from the title)
            # Select words with a length greater than 3, up to a maximum of 5.
            simple_keywords = [
                word.strip()
                for word in potential_title.lower().split()
                if len(word.strip()) > 3
            ][:5]

            #  3. Extract the chapter structure (first 5 paragraphs or chapters)
            # Send only the title, not the full content.
            sections = []
            current_section_lines = []

            for line in lines[:100]:  # View only the first 100 lines
                line_stripped = line.strip()
                if not line_stripped:
                    continue

                # Determine if it is a chapter title (simple rule: shorter line, or contains numbers).
                if len(line_stripped) < 100 and (
                    line_stripped[0].isdigit()
                    or line_stripped.isupper()
                    or any(
                        marker in line_stripped.lower()
                        for marker in ["step", "phase", "stage", "chapter"]
                    )
                ):
                    if current_section_lines:
                        # Save the previous section (keeping only the first 200 words as a summary).
                        content_preview = " ".join(current_section_lines)[:200]
                        sections.append(
                            {
                                "title": current_section_lines[0][:150],
                                "content": content_preview,  #  Keep only the first 200 characters
                                "level": 1,
                            }
                        )
                        current_section_lines = [line_stripped]
                    else:
                        current_section_lines = [line_stripped]
                else:
                    if (
                        len(current_section_lines) < 3
                    ):  # Each section can retain a maximum of 3 lines of preview.
                        current_section_lines.append(line_stripped)

            # Save the last section
            if current_section_lines:
                content_preview = " ".join(current_section_lines)[:200]
                sections.append(
                    {
                        "title": current_section_lines[0][:150],
                        "content": content_preview,
                        "level": 1,
                    }
                )

            # If no sections are extracted, use simple segmentation.
            if not sections:
                # Simple segmentation: 500 words per section
                text_parts = [
                    request.text[i : i + 500]
                    for i in range(0, min(len(request.text), 2500), 500)
                ]
                sections = [
                    {
                        "title": f"Section {i+1}",
                        "content": part[:200]
                        + "...",  #  Only the first 200 words of each section are retained.
                        "level": 1,
                    }
                    for i, part in enumerate(text_parts)
                ]

            #  4. Create optimized metadata (refer to the Lock ON structure).
            metadata = {
                "doc_id": f"doc-{generate(size=12)}",
                "title": potential_title,  #  Real title
                "subject": potential_title,
                "language": "en",
                "bypass_local_llm": True,
                #  Key fields
                "keywords": simple_keywords,  #  5-10 keywords
                #  sections: Contains only chapter titles and a preview of the first 200 words.
                "sections": sections[:10],  # Up to 10 sections
                #  facets: Simple topic categorization
                "facets": {
                    "main_topic": {
                        "summary": potential_title,
                        "items": [
                            {
                                "value": kw,
                                "evidence": "",
                                "location": "",
                                "confidence": 0.8,
                            }
                            for kw in simple_keywords
                        ],
                    }
                },
                #  key_values: Key-value pairs containing key information
                "key_values": [
                    {"key": "document_title", "value": potential_title},
                    {"key": "processing_mode", "value": "direct"},
                    {"key": "section_count", "value": str(len(sections))},
                ],
                #  tags: using keywords
                "tags": simple_keywords,
                # Other required fields (keep them empty)
                "triples": [],
                "questions": [],
                "risks": [],
                "actions_todo": [],
                "metrics": [],
                "tables": [],
                "figures": [],
                "extra": {
                    "processing_mode": "direct",
                    "note": "Extracted structure without full text to reduce prompt size",
                    "original_length": len(request.text),
                    "truncated": True,
                },
            }

            # Do not add raw_text or full_content!
            # ChatGPT does not require the complete original text, only the structured information.

            framework_result = process_with_global_llm(
                metadata=metadata, model=request.model, use_mock=False
            )
            print(" Global LLM completed")

        # 🔧 Modification: Supports multiple POVs / multiple frameworks in the results.
        #  Modification: Supports multiple POVs / multiple frameworks in the results.
        frameworks = framework_result.get("frameworks", [framework_result])

        print(f" Framework generation completed: {len(frameworks)} framework(s)")

        #  The generated data is returned directly without being saved to the database (it is saved to Firebase by the front end).
        return GenerateResponse(
            success=True,
            framework_id=None,  # The front-end will have an ID after creation.
            framework=frameworks[0] if frameworks else None,
            frameworks=frameworks,
            metadata=metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f" Error in generate_from_text: {str(e)}")
        import traceback

        traceback.print_exc()
        return GenerateResponse(success=False, error=str(e))


@router.post("/generate-from-file", response_model=GenerateResponse)
async def generate_from_file(
    file: UploadFile = File(...),
    use_global_llm: bool = True,
    model: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Generate a framework from uploaded files (login required)

    Call chain: Front-end file → Local LLM → Global LLM → Save to database → Return to framework
    """
    temp_path = None

    try:
        # Verify file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check file type
        allowed_extensions = {".txt", ".pdf", ".doc", ".docx", ".md"}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
            )

        # Check file size (10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(content)
            temp_path = tmp.name

        print(f" File saved to: {temp_path}")

        if use_global_llm:
            print(" Step 1: Building deterministic file metadata...")
            file_content = read_file_content(temp_path, file.filename)
            usable_content = (
                file_content
                if file_content and not file_content.startswith("[Unable to read")
                else ""
            )
            metadata = build_deterministic_file_metadata(
                [file.filename],
                [usable_content],
            )
            print(
                f" File metadata completed. Extracted {len(metadata)} metadata fields"
            )
        else:
            print(" Step 1: Processing with legacy local LLM...")
            metadata = process_with_local_llm(temp_path, is_file=True)
            print(f" Local LLM completed. Extracted {len(metadata)} metadata fields")

        # Step 2: Global LLM Generation Framework
        print(" Step 2: Processing with configured LLM Provider...")
        framework_result = process_with_global_llm(  #  MODIFIED
            metadata=metadata, model=model, use_mock=False
        )
        print(" Global LLM completed. Framework generated")

        #  MODIFIED: Supports multiple POV outputs
        frameworks = framework_result.get("frameworks", [framework_result])

        #  Step 3: Save to database
        print("💾 Step 3: Saving framework(s) to database...")
        saved_ids = []  #  MODIFIED
        for fw_data in frameworks:  #  MODIFIED
            db_framework = save_framework_to_db(  #  MODIFIED
                framework_data=fw_data,  #  MODIFIED
                metadata_dict=metadata,
                creator_id=user_id,
                db=db,
            )
            saved_ids.append(db_framework.id)  #  MODIFIED
        print(f" All frameworks saved: {len(saved_ids)} total")  #  MODIFIED

        #  MODIFIED: Returns both single and multiple values ​​(backwards compatible).
        return GenerateResponse(
            success=True,
            framework_id=saved_ids[0] if saved_ids else None,  #  MODIFIED
            framework=frameworks[0] if frameworks else None,  #  MODIFIED
            frameworks=frameworks,  #  MODIFIED
            metadata=metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f" Error in generate_from_file: {str(e)}")
        import traceback

        traceback.print_exc()
        return GenerateResponse(success=False, error=str(e))
    finally:
        # Clean up temporary files
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass


@router.post("/generate-from-files", response_model=GenerateResponse)
async def generate_from_files(
    files: List[UploadFile] = File(...),
    use_global_llm: bool = True,
    model: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Generate a framework from multiple files (login required)

    Multiple files will be merged.
    """
    temp_paths = []

    try:
        if not files or len(files) == 0:
            raise HTTPException(status_code=400, detail="No files provided")

        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Too many files (max 10)")

        # Save all files to a temporary directory
        for file in files:
            if not file.filename:
                continue

            file_ext = Path(file.filename).suffix.lower()
            allowed_extensions = {".txt", ".pdf", ".doc", ".docx", ".md"}

            if file_ext not in allowed_extensions:
                continue

            content = await file.read()
            if len(content) > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=400, detail=f"File {file.filename} too large"
                )

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
                tmp.write(content)
                temp_paths.append(tmp.name)

        if not temp_paths:
            raise HTTPException(status_code=400, detail="No valid files")

        print(f" Saved {len(temp_paths)} files")

        #  Whether to use Local LLM depends on use_global_llm.
        if not use_global_llm:
            #  Lock ON: Privacy Protection Mode
            print(" Step 1: Processing files with Local LLM (Privacy Protection)...")
            all_metadata = []

            for temp_path in temp_paths:
                metadata = process_with_local_llm(temp_path, is_file=True)
                all_metadata.append(metadata)

            merged_metadata = all_metadata[0] if all_metadata else {}
            if len(all_metadata) > 1:
                merged_metadata["source_count"] = len(all_metadata)
                merged_metadata["merged_from_multiple_files"] = True

            print(f" Local LLM completed. Processed {len(temp_paths)} files")

            print(" Step 2: Processing with Global LLM...")
            framework_result = process_with_global_llm(
                metadata=merged_metadata, model=model, use_mock=False
            )
            print(" Global LLM completed")
        else:
            #  Lock OFF: Quick Mode
            print(" Processing with Global LLM (Fast Mode - No Local Processing)...")

            # Read all file contents
            file_contents = []
            file_names = []
            for i, temp_path in enumerate(temp_paths):
                try:
                    # Get filename
                    original_filename = (
                        files[i].filename if i < len(files) else f"file_{i+1}"
                    )
                    file_names.append(original_filename)

                    # Use smart read function Fix .docx garbled issue
                    content = read_file_content(temp_path, original_filename)
                    if content and not content.startswith("[Unable to read"):
                        file_contents.append(content)
                    else:
                        print(f"Warning: {content}")

                except Exception as e:
                    print(f"Warning: Could not read file {temp_path}: {e}")

            # 1. Intelligent title extraction
            if len(file_contents) == 1:
                # Single file: Use the first line or the filename
                lines = file_contents[0].strip().split("\n")
                potential_title = (
                    lines[0][:150].strip()
                    if lines and len(lines[0].strip()) > 10
                    else file_names[0]
                )
            else:
                # Multiple files: Use combined descriptions
                lines = file_contents[0].strip().split("\n") if file_contents else []
                if lines and len(lines[0].strip()) > 10:
                    potential_title = lines[0][:150].strip()
                else:
                    potential_title = f"Framework from {len(file_names)} files"

            #  2. Simple Keyword Extraction
            simple_keywords = [
                word.strip()
                for word in potential_title.lower().split()
                if len(word.strip()) > 3
            ][:5]

            #  3. Extract sections (extract from all files, but keep only the first 200 words of each section)
            all_sections = []

            for idx, content in enumerate(file_contents):
                file_name = (
                    file_names[idx] if idx < len(file_names) else f"File {idx+1}"
                )
                lines = content.strip().split("\n")

                # Create sections for each file
                current_section_lines = []

                for line in lines[
                    :50
                ]:  # Only the first 50 lines of each file are viewed.
                    line_stripped = line.strip()
                    if not line_stripped:
                        continue

                    # Determine if it is a chapter title
                    if len(line_stripped) < 100 and (
                        line_stripped[0].isdigit()
                        or line_stripped.isupper()
                        or any(
                            marker in line_stripped.lower()
                            for marker in ["step", "phase", "stage", "chapter"]
                        )
                    ):
                        if current_section_lines:
                            content_preview = " ".join(current_section_lines)[:200]
                            all_sections.append(
                                {
                                    "title": f"{file_name}: {current_section_lines[0][:100]}",
                                    "content": content_preview,  #  Keep only the first 200 characters
                                    "level": 1,
                                    "source_file": file_name,
                                }
                            )
                            current_section_lines = [line_stripped]
                        else:
                            current_section_lines = [line_stripped]
                    else:
                        if len(current_section_lines) < 3:
                            current_section_lines.append(line_stripped)

                # Save the last section
                if current_section_lines:
                    content_preview = " ".join(current_section_lines)[:200]
                    all_sections.append(
                        {
                            "title": f"{file_name}: {current_section_lines[0][:100]}",
                            "content": content_preview,
                            "level": 1,
                            "source_file": file_name,
                        }
                    )

            # If no sections are extracted, create a simple section for each file.
            if not all_sections:
                all_sections = [
                    {
                        "title": file_names[i]
                        if i < len(file_names)
                        else f"File {i+1}",
                        "content": content[:200]
                        + "...",  #  Keep only the first 200 characters
                        "level": 1,
                        "source_file": file_names[i]
                        if i < len(file_names)
                        else f"File {i+1}",
                    }
                    for i, content in enumerate(file_contents)
                ]

            #  4. Create optimized metadata
            merged_metadata = {
                "doc_id": f"doc-{generate(size=12)}",
                "title": potential_title,  #  real title
                "subject": potential_title,
                "language": "en",
                "bypass_local_llm": True,
                #  keywords
                "keywords": simple_keywords,
                #  sections: Contains only chapter titles and a preview of the first 200 words.
                "sections": all_sections[:15],  # Up to 15 sections
                #  facets
                "facets": {
                    "main_topic": {
                        "summary": potential_title,
                        "items": [
                            {
                                "value": kw,
                                "evidence": "",
                                "location": "",
                                "confidence": 0.8,
                            }
                            for kw in simple_keywords
                        ],
                    },
                    "source_files": {
                        "summary": f"Content from {len(file_contents)} file(s)",
                        "items": [
                            {
                                "value": name,
                                "evidence": "",
                                "location": "",
                                "confidence": 1.0,
                            }
                            for name in file_names
                        ],
                    },
                },
                #  key_values
                "key_values": [
                    {"key": "document_title", "value": potential_title},
                    {"key": "file_count", "value": str(len(file_contents))},
                    {"key": "processing_mode", "value": "direct"},
                    {"key": "source_files", "value": ", ".join(file_names[:3])},
                ],
                #  tags
                "tags": simple_keywords,
                # Other required fields
                "source_count": len(file_contents),
                "source_files": file_names,
                "triples": [],
                "questions": [],
                "risks": [],
                "actions_todo": [],
                "metrics": [],
                "tables": [],
                "figures": [],
                "extra": {
                    "processing_mode": "direct",
                    "note": "Extracted structure without full text to reduce prompt size",
                    "file_names": file_names,
                    "total_length": sum(len(c) for c in file_contents),
                    "truncated": True,
                },
            }

            #  Key point: Do not add raw_text, full_content, or the complete combined_text!

            framework_result = process_with_global_llm(
                metadata=merged_metadata, model=model, use_mock=False
            )
            print(" Global LLM completed")

        #  MODIFIED: Supports multiple POV outputs
        frameworks = framework_result.get("frameworks", [framework_result])

        #  Step 3: Generate framework IDs (the frontend will save them to Firebase).
        print(
            "💾 Step 3: Generating framework IDs (data will be saved to Firebase by frontend)..."
        )

        saved_ids = []
        for fw_data in frameworks:
            # Generate a unique ID for each framework
            fw_id = f"fw_{generate(size=12)}"
            fw_data["id"] = fw_id  # Add ID to framework data
            saved_ids.append(fw_id)

        print(f" Generated {len(saved_ids)} framework IDs: {saved_ids}")

        #  MODIFIED: Returns both single and multiple [MODIFIED] values.
        return GenerateResponse(
            success=True,
            framework_id=saved_ids[0] if saved_ids else None,
            framework=frameworks[0] if frameworks else None,
            frameworks=frameworks,
            metadata=merged_metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f" Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return GenerateResponse(success=False, error=str(e))
    finally:
        # Clean up all temporary files
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass

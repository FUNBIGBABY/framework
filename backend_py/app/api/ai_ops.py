import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth import get_current_user_id
from ..services.llm import LLMProviderError, get_llm_provider
from .frameworks_shared import (
    RegenerateRequest,
    process_with_global_llm,
    process_with_local_llm,
)


router = APIRouter()


@router.post("/regenerate")
async def regenerate_framework(
    request: RegenerateRequest, current_user_id: str = Depends(get_current_user_id)
):
    """
    Regenerate the framework (improved by user editing).

    Users can choose:
    1. Provider processing - uses the configured LLM Provider
    2. Legacy local processing - requires ENABLE_LEGACY_LLM=true
    """
    try:
        if request.use_local:
            # ========== Legacy Local Processing Mode ==========
            print(" Using legacy local metadata extraction")
            framework_text = convert_framework_to_text(request.framework)
            metadata = process_with_local_llm(framework_text, is_file=False)
            improved_framework = process_with_global_llm(metadata=metadata)

            return {
                "success": True,
                "framework": improved_framework,
                "method": "local",
                "message": "Framework regenerated using legacy local metadata extraction and the configured LLM Provider",
            }

        else:
            # ========== Cloud Processing Mode (Recommended) =========
            print("Using Cloud Processing (LLM Provider)")

            system_prompt = (
                "You are a framework improvement assistant. "
                "The user has edited a framework and wants you to review and improve it. "
                "CRITICAL: Keep ALL user modifications intact. Only fill in missing parts and suggest improvements. "
                "Return the improved framework as valid JSON matching the original structure."
            )

            user_prompt = (
                "Here is a framework that the user has edited:\n\n"
                f"{json.dumps(request.framework, indent=2)}\n\n"
                "Please:\n"
                "1. **Keep all user modifications intact** (especially steps, risks, escalation)\n"
                "2. Fill in missing sections if any:\n"
                "   - Add 'trigger_context' or 'pov' if missing\n"
                "   - Add 'inputs_required' if missing\n"
                "   - Add 'research_required' if missing\n"
                "   - Add 'attribution' if appropriate\n"
                "   - Add 'quadrant' (QI/QII/QIII/QIV) if appropriate\n"
                "3. Ensure consistency across all sections\n"
                "4. Improve descriptions to be more specific and actionable\n"
                "5. Return the complete improved framework as JSON\n\n"
                "IMPORTANT: Do NOT remove or significantly change user's content. Only enhance and complete."
            )

            try:
                improved_framework = get_llm_provider().generate_json(
                    [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    reasoning=True,
                    temperature=0.3,
                    timeout=180.0,
                )
            except (LLMProviderError, NotImplementedError) as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc

            return {
                "success": True,
                "framework": improved_framework,
                "method": "cloud",
                "message": "Framework regenerated using cloud processing",
            }

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        print(" Regeneration Error:")
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500, detail=f"Failed to regenerate framework: {str(e)}"
        )


def convert_framework_to_text(framework: dict) -> str:
    """
    Convert the frame JSON back to text (for local LLM processing)
    This is a simplified version used to simulate the original document.
    """
    parts = []

    # Title
    metadata = framework.get("metadata", {})
    title = metadata.get("title", "Framework")
    parts.append(f"# {title}\n")

    # Steps
    steps = framework.get("steps", [])
    if steps:
        parts.append("\n## Framework Steps\n")
        for step in steps:
            parts.append(f"\n### {step.get('name', 'Step')}")
            parts.append(step.get("description", ""))
            sub_steps = step.get("subSteps", [])
            if sub_steps:
                for sub in sub_steps:
                    parts.append(f"- {sub}")

    # Risks
    risks = framework.get("risks", [])
    if risks:
        parts.append("\n## Risks\n")
        for risk in risks:
            parts.append(f"\n### {risk.get('title', 'Risk')}")
            parts.append(risk.get("description", ""))

    # Escalation
    escalation = framework.get("escalation", [])
    if escalation:
        parts.append("\n## Escalation Points\n")
        for esc in escalation:
            parts.append(f"- When: {esc.get('trigger', 'Unknown')}")
            parts.append(f"  Action: {esc.get('action', 'Escalate')}")

    return "\n".join(parts)


# ============= AI Merge Endpoint =============


class AIMergeRequest(BaseModel):
    """AI merge request model"""

    frameworks: List[dict]  # Multiple frameworks selected by the user


@router.post("/ai-merge")
async def ai_merge_frameworks(
    request: AIMergeRequest, current_user_id: str = Depends(get_current_user_id)
):
    """
    Use AI to intelligently merge multiple frameworks.

    Requires a valid JWT before any merge or mock-merge logic can run.
    """
    try:
        # Validate input
        if not request.frameworks or len(request.frameworks) < 2:
            raise HTTPException(
                status_code=400, detail="Please select at least 2 frameworks to merge"
            )

        if len(request.frameworks) > 10:
            raise HTTPException(
                status_code=400, detail="Cannot merge more than 10 frameworks at once"
            )

        print(f"🔀 AI Merge: Merging {len(request.frameworks)} frameworks")

        # Ready to merge prompt
        frameworks_text = []
        for i, fw in enumerate(request.frameworks, 1):
            frameworks_text.append(f"\n{'='*60}")
            frameworks_text.append(f"FRAMEWORK {i}: {fw.get('name', 'Unnamed')}")
            frameworks_text.append(f"{'='*60}\n")

            # Description
            if fw.get("description"):
                frameworks_text.append(f"Description:\n{fw['description']}\n")

            # Sub-steps
            if fw.get("subSteps"):
                frameworks_text.append("Sub-steps:")
                for j, step in enumerate(fw["subSteps"], 1):
                    frameworks_text.append(f"  {j}. {step}")
                frameworks_text.append("")

        combined_text = "\n".join(frameworks_text)

        system_prompt = (
            "You are a framework merging assistant. "
            "Your task is to intelligently combine multiple frameworks into one cohesive framework. "
            "You should:\n"
            "1. Identify common themes and consolidate similar content\n"
            "2. Remove redundancy while preserving unique insights from each framework\n"
            "3. Organize the merged content logically\n"
            "4. Create a clear, comprehensive description that captures all key aspects\n"
            "5. Combine sub-steps in a logical order\n"
            "6. Generate an appropriate name for the merged framework\n\n"
            "Return ONLY a valid JSON object with this structure:\n"
            "{\n"
            '  "name": "Merged Framework Name",\n'
            '  "description": "Comprehensive description...",\n'
            '  "subSteps": ["Step 1", "Step 2", ...]\n'
            "}"
        )

        user_prompt = (
            f"Please merge these {len(request.frameworks)} frameworks into one:\n\n"
            f"{combined_text}\n\n"
            "Create a new framework that:\n"
            "- Captures the essence of all input frameworks\n"
            "- Eliminates redundancy and contradictions\n"
            "- Provides a clear, actionable structure\n"
            "- Has a descriptive name that reflects the merged content\n\n"
            "Return the merged framework as JSON."
        )

        try:
            merged_framework = get_llm_provider().generate_json(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                reasoning=True,
                temperature=0.4,
                timeout=300.0,
            )
        except (LLMProviderError, NotImplementedError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        # Ensure required fields exist
        if not merged_framework.get("name"):
            merged_framework["name"] = "AI Merged Framework"

        if not merged_framework.get("description"):
            merged_framework["description"] = ""

        if not merged_framework.get("subSteps"):
            merged_framework["subSteps"] = []

        print(f" Successfully merged into: {merged_framework['name']}")

        return {"success": True, "merged_framework": merged_framework}

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        print(" AI Merge Error:")
        print(traceback.format_exc())

        return {"success": False, "error": str(e)}


# ============= AI Fill Endpoint =============


class AIFillRequest(BaseModel):
    """AI Fill request model"""

    artefact_name: str
    artefact_summary: str = ""
    existing_sections: List[dict] = []  # [{heading: str, body: str}]
    sections_to_fill: List[str] = []  # List of section headings to fill


def parse_ai_json_response(text):
    """
    Parse JSON from AI response, handling common issues like markdown code blocks
    """
    import json
    import re

    # Remove markdown code blocks if present
    text = text.strip()

    # Remove ```json ... ``` or ``` ... ```
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    # Try to find JSON array in the text
    # Look for [ ... ] pattern
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        text = match.group(0)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Attempted to parse: {text[:500]}...")
        raise


@router.post("/ai-fill")
async def ai_fill_sections(
    request: AIFillRequest, current_user_id: str = Depends(get_current_user_id)
):
    """
    Use AI to fill empty section content based on context
    """
    try:
        if not request.sections_to_fill:
            return {
                "success": True,
                "filled_sections": [],
                "message": "No sections to fill",
            }

        print(
            f"✨ AI Fill: Filling {len(request.sections_to_fill)} sections for '{request.artefact_name}'"
        )

        # Build context from existing sections
        existing_context = ""
        if request.existing_sections:
            existing_context = "\n\nExisting sections for context:\n"
            for sec in request.existing_sections:
                existing_context += (
                    f"- {sec.get('heading', 'Section')}: {sec.get('body', '')}\n"
                )

        system_prompt = (
            "You are an expert document writer. Your task is to fill in content for document sections. "
            "If section names are numbers or very short, infer logical section topics based on the document context. "
            "You MUST return ONLY a valid JSON array with no additional text, markdown, or explanation. "
            "Do not wrap the response in code blocks. Just output the raw JSON array."
        )

        sections_list = ", ".join([f'"{s}"' for s in request.sections_to_fill])

        # Check if sections are just numbers - provide extra context
        has_number_sections = any(s.strip().isdigit() for s in request.sections_to_fill)
        extra_instruction = ""
        if has_number_sections:
            extra_instruction = """
IMPORTANT: Some sections are numbered (e.g., "3", "4"). Based on the document type and existing sections,
infer what these numbered sections should logically contain. For example:
- For compliance documents: risk analysis, mitigation steps, monitoring procedures
- For technical documents: implementation details, testing procedures, maintenance
- Follow the pattern of existing numbered sections if present."""

        user_prompt = f"""Document: {request.artefact_name}
Summary: {request.artefact_summary or 'A professional document'}
{existing_context}
{extra_instruction}

Write professional content for these sections: {sections_list}

Output format (return ONLY this JSON array, nothing else):
[{{"heading": "Section Name", "body": "Professional content here..."}}]

Requirements:
- Each body should be 2-3 sentences of relevant, professional content
- Infer appropriate content based on document type and context
- Be specific and actionable, not generic"""

        try:
            filled_sections = get_llm_provider().generate_json(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                reasoning=True,
                temperature=0.4,
                timeout=120.0,
            )
        except (LLMProviderError, NotImplementedError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        # Validate response format
        if not isinstance(filled_sections, list):
            filled_sections = [filled_sections]

        # Ensure all requested sections are filled
        filled_headings = {s.get("heading") for s in filled_sections}
        for section_name in request.sections_to_fill:
            if section_name not in filled_headings:
                filled_sections.append(
                    {
                        "heading": section_name,
                        "body": f"Content for {section_name} section.",
                    }
                )

        print(f"✅ Successfully filled {len(filled_sections)} sections")
        return {"success": True, "filled_sections": filled_sections}

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        print("❌ AI Fill Error:")
        print(traceback.format_exc())
        return {"success": False, "error": str(e), "filled_sections": []}

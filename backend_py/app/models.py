from datetime import datetime

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from .db import Base


JSONB = postgresql.JSONB
JSONB_OBJECT_DEFAULT = sa.text("'{}'::jsonb")
JSONB_ARRAY_DEFAULT = sa.text("'[]'::jsonb")


class Material(Base):
    __tablename__ = "materials"

    id = sa.Column(sa.String, primary_key=True, index=True)  # e.g. "mat_xxx"
    type = sa.Column(sa.String, nullable=False)  # text,pdf,doc,docx,file
    status = sa.Column(sa.String, nullable=False, default="available")

    # Keep bytes out of DB unless the legacy endpoint explicitly stores them.
    storage_url = sa.Column(sa.String, nullable=True)

    # Existing material APIs still store this as a JSON string.
    metadata_json = sa.Column(sa.Text, nullable=True)

    filename = sa.Column(sa.String, nullable=True)
    mime = sa.Column(sa.String, nullable=True)
    sizebyte = sa.Column(sa.Integer, nullable=True)
    contentbytes = sa.Column(sa.LargeBinary, nullable=True)

    # Nullable only to quarantine pre-ownership rows. All active creation paths
    # set this from the authenticated user, and authenticated retrieval excludes
    # rows without an owner.
    owner_id = sa.Column(
        sa.String,
        sa.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    owner = relationship("User", back_populates="materials")

    created = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.String, primary_key=True, index=True)  # e.g. "user_xxx"
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    username = sa.Column(sa.String, unique=True, nullable=False, index=True)
    password_hash = sa.Column(sa.String, nullable=False)  # Argon2id password hash
    refresh_token_version = sa.Column(
        sa.Integer, nullable=False, default=0, server_default="0"
    )
    is_disabled = sa.Column(
        sa.Boolean, nullable=False, default=False, server_default=sa.false(), index=True
    )
    disabled_at = sa.Column(sa.DateTime, nullable=True)

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    last_login = sa.Column(sa.DateTime, nullable=True)

    frameworks = relationship(
        "Framework", back_populates="creator", cascade="all, delete-orphan"
    )
    materials = relationship("Material", back_populates="owner", passive_deletes=True)


class Framework(Base):
    __tablename__ = "frameworks"

    id = sa.Column(sa.String, primary_key=True, index=True)  # e.g. "fw_xxx"
    title = sa.Column(sa.String, nullable=False)
    version = sa.Column(sa.String, default="1.0.0")
    family = sa.Column(sa.String, nullable=False, index=True)
    confidence = sa.Column(sa.Float, default=0.0)
    pov = sa.Column(sa.String, nullable=True)
    is_public = sa.Column(
        sa.Boolean, nullable=False, default=False, server_default=sa.false(), index=True
    )
    category = sa.Column(sa.String, nullable=True, index=True)
    tags_json = sa.Column(JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT)
    published_at = sa.Column(sa.DateTime, nullable=True, index=True)

    creator_id = sa.Column(
        sa.String, sa.ForeignKey("users.id"), nullable=False, index=True
    )
    creator = relationship("User", back_populates="frameworks")
    artefact_rows = relationship(
        "Artefact", back_populates="framework", cascade="all, delete-orphan"
    )

    metadata_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT
    )
    steps_json = sa.Column(JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT)
    artefacts_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT
    )
    risks_json = sa.Column(JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT)
    escalation_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT
    )

    raw_framework_json = sa.Column(JSONB, nullable=True)
    raw_metadata_json = sa.Column(JSONB, nullable=True)

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, index=True)
    updated_at = sa.Column(
        sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Artefact(Base):
    __tablename__ = "artefacts"

    id = sa.Column(sa.String, primary_key=True)
    framework_id = sa.Column(
        sa.String,
        sa.ForeignKey("frameworks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = sa.Column(sa.String, nullable=False)
    artefact_type = sa.Column(sa.String, nullable=True, server_default="custom")
    content_json = sa.Column(JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT)
    metadata_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT
    )
    ord = sa.Column(sa.Integer, nullable=False, default=0, server_default="0")
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=datetime.utcnow
    )

    framework = relationship("Framework", back_populates="artefact_rows")

    __table_args__ = (sa.Index("ix_artefacts_framework_id_ord", "framework_id", "ord"),)


# Preset Framework Groups (AI selects from these)
FRAMEWORK_GROUPS = [
    "Financial",
    "Healthcare",
    "Legal",
    "Technology",
    "Education",
    "Marketing",
    "Operations",
    "Human Resources",
    "Sales",
    "Other",
]


class SyncedVectorItem(Base):
    __tablename__ = "synced_vector_items"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    doc_id = sa.Column(sa.String, nullable=False, index=True)
    vs_id = sa.Column(sa.String, nullable=False, index=True)
    source = sa.Column(sa.String, nullable=True)
    first_synced_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    last_synced_at = sa.Column(
        sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (sa.UniqueConstraint("doc_id", "vs_id", name="uix_doc_vs"),)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(
        sa.String,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = sa.Column(sa.String, nullable=False, server_default="pending")
    model = sa.Column(sa.String, nullable=True)
    selected_skill = sa.Column(sa.String, nullable=True)
    skill_version = sa.Column(sa.String, nullable=True)
    allowed_tools_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT
    )
    skill_input_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT
    )
    skill_output_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT
    )
    started_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    ended_at = sa.Column(sa.DateTime, nullable=True)
    total_tokens_in = sa.Column(sa.Integer, nullable=False, server_default="0")
    total_tokens_out = sa.Column(sa.Integer, nullable=False, server_default="0")
    cost_micros = sa.Column(sa.BigInteger, nullable=False, server_default="0")
    error = sa.Column(sa.Text, nullable=True)


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = sa.Column(sa.String, primary_key=True)
    run_id = sa.Column(
        sa.String,
        sa.ForeignKey("agent_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = sa.Column(sa.String, nullable=False)
    content_text = sa.Column(sa.Text, nullable=True)
    content_json = sa.Column(JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT)
    tool_call_id = sa.Column(sa.String, nullable=True)
    parent_id = sa.Column(
        sa.String, sa.ForeignKey("agent_messages.id", ondelete="SET NULL")
    )
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())


class AgentToolInvocation(Base):
    __tablename__ = "agent_tool_invocations"

    id = sa.Column(sa.String, primary_key=True)
    run_id = sa.Column(
        sa.String,
        sa.ForeignKey("agent_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    message_id = sa.Column(
        sa.String, sa.ForeignKey("agent_messages.id", ondelete="SET NULL")
    )
    tool_name = sa.Column(sa.String, nullable=False)
    tool_version = sa.Column(sa.String, nullable=True)
    input_schema_version = sa.Column(sa.String, nullable=True)
    output_schema_version = sa.Column(sa.String, nullable=True)
    args_json = sa.Column(JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT)
    result_json = sa.Column(JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT)
    latency_ms = sa.Column(sa.Integer, nullable=True)
    status = sa.Column(sa.String, nullable=False, server_default="pending")


class Document(Base):
    __tablename__ = "documents"

    id = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(
        sa.String,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = sa.Column(sa.String, nullable=False)
    source_type = sa.Column(sa.String, nullable=True)
    source_uri = sa.Column(sa.String, nullable=True)
    hash = sa.Column(sa.String, nullable=True, index=True)
    mime = sa.Column(sa.String, nullable=True)
    size_bytes = sa.Column(sa.BigInteger, nullable=True)
    status = sa.Column(sa.String, nullable=False, server_default="pending")
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    deleted_at = sa.Column(sa.DateTime, nullable=True)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = sa.Column(sa.String, primary_key=True)
    document_id = sa.Column(
        sa.String,
        sa.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ord = sa.Column(sa.Integer, nullable=False, default=0, server_default="0")
    text = sa.Column(sa.Text, nullable=False)
    token_count = sa.Column(sa.Integer, nullable=False, server_default="0")
    embedding = sa.Column(Vector(1024), nullable=True)
    embedding_model = sa.Column(sa.String, nullable=True)
    embedding_dim = sa.Column(sa.Integer, nullable=False, server_default="1024")

    __table_args__ = (
        sa.Index("ix_document_chunks_document_id_ord", "document_id", "ord"),
    )


class Citation(Base):
    __tablename__ = "citations"

    id = sa.Column(sa.String, primary_key=True)
    run_id = sa.Column(
        sa.String, sa.ForeignKey("agent_runs.id", ondelete="SET NULL"), index=True
    )
    message_id = sa.Column(
        sa.String, sa.ForeignKey("agent_messages.id", ondelete="SET NULL")
    )
    document_id = sa.Column(
        sa.String, sa.ForeignKey("documents.id", ondelete="SET NULL"), index=True
    )
    chunk_id = sa.Column(
        sa.String, sa.ForeignKey("document_chunks.id", ondelete="SET NULL"), index=True
    )
    framework_id = sa.Column(
        sa.String, sa.ForeignKey("frameworks.id", ondelete="SET NULL"), index=True
    )
    version = sa.Column(sa.String, nullable=True)


class WikiBuild(Base):
    __tablename__ = "wiki_builds"

    id = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(
        sa.String,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = sa.Column(sa.String, nullable=False, server_default="pending")
    source_hash = sa.Column(sa.String, nullable=True)
    started_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    ended_at = sa.Column(sa.DateTime, nullable=True)
    metrics_json = sa.Column(JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT)


class WikiPage(Base):
    __tablename__ = "wiki_pages"

    id = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(
        sa.String,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = sa.Column(sa.String, nullable=False)
    slug = sa.Column(sa.String, nullable=False, index=True)
    summary = sa.Column(sa.Text, nullable=True)
    body = sa.Column(sa.Text, nullable=True)
    source_refs_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT
    )
    version = sa.Column(sa.String, nullable=False, server_default="1")
    build_id = sa.Column(
        sa.String, sa.ForeignKey("wiki_builds.id", ondelete="SET NULL")
    )
    status = sa.Column(sa.String, nullable=False, server_default="draft")
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now())


class WikiClaim(Base):
    __tablename__ = "wiki_claims"

    id = sa.Column(sa.String, primary_key=True)
    page_id = sa.Column(
        sa.String,
        sa.ForeignKey("wiki_pages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    claim_text = sa.Column(sa.Text, nullable=False)
    confidence = sa.Column(sa.Float, nullable=True)
    source_chunk_ids_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT
    )
    status = sa.Column(sa.String, nullable=False, server_default="active")


class WikiLink(Base):
    __tablename__ = "wiki_links"

    id = sa.Column(sa.String, primary_key=True)
    from_page_id = sa.Column(
        sa.String,
        sa.ForeignKey("wiki_pages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    to_page_id = sa.Column(
        sa.String,
        sa.ForeignKey("wiki_pages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relation = sa.Column(sa.String, nullable=True)
    confidence = sa.Column(sa.Float, nullable=True)


class WikiEntity(Base):
    __tablename__ = "wiki_entities"

    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String, nullable=False, index=True)
    type = sa.Column(sa.String, nullable=True)
    canonical_page_id = sa.Column(
        sa.String, sa.ForeignKey("wiki_pages.id", ondelete="SET NULL")
    )
    aliases_json = sa.Column(JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT)


class WikiEvalQuestion(Base):
    __tablename__ = "wiki_eval_questions"

    id = sa.Column(sa.String, primary_key=True)
    build_id = sa.Column(
        sa.String,
        sa.ForeignKey("wiki_builds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question = sa.Column(sa.Text, nullable=False)
    expected_refs_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_ARRAY_DEFAULT
    )
    last_result_json = sa.Column(
        JSONB, nullable=False, server_default=JSONB_OBJECT_DEFAULT
    )

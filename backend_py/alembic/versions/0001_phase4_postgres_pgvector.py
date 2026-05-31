"""phase 4 postgres pgvector baseline

Revision ID: 0001_phase4_postgres_pgvector
Revises:
Create Date: 2026-05-31
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql


revision: str = "0001_phase4_postgres_pgvector"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


JSONB = postgresql.JSONB(astext_type=sa.Text())
JSONB_OBJECT = sa.text("'{}'::jsonb")
JSONB_ARRAY = sa.text("'[]'::jsonb")
NOW = sa.text("now()")


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "materials",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("storage_url", sa.String(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("filename", sa.String(), nullable=True),
        sa.Column("mime", sa.String(), nullable=True),
        sa.Column("sizebyte", sa.Integer(), nullable=True),
        sa.Column("contentbytes", sa.LargeBinary(), nullable=True),
        sa.Column("created", sa.DateTime(timezone=True), server_default=NOW),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_materials_id", "materials", ["id"])

    op.create_table(
        "users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "frameworks",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("family", sa.String(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("pov", sa.String(), nullable=True),
        sa.Column("creator_id", sa.String(), nullable=False),
        sa.Column("metadata_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("steps_json", JSONB, server_default=JSONB_ARRAY, nullable=False),
        sa.Column("artefacts_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("risks_json", JSONB, server_default=JSONB_ARRAY, nullable=False),
        sa.Column("escalation_json", JSONB, server_default=JSONB_ARRAY, nullable=False),
        sa.Column("raw_framework_json", JSONB, nullable=True),
        sa.Column("raw_metadata_json", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_frameworks_id", "frameworks", ["id"])
    op.create_index("ix_frameworks_family", "frameworks", ["family"])
    op.create_index("ix_frameworks_creator_id", "frameworks", ["creator_id"])
    op.create_index("ix_frameworks_created_at", "frameworks", ["created_at"])

    op.create_table(
        "artefacts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("framework_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("artefact_type", sa.String(), server_default=sa.text("'custom'")),
        sa.Column("content_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("metadata_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("ord", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=NOW),
        sa.Column("updated_at", sa.DateTime(), server_default=NOW),
        sa.ForeignKeyConstraint(
            ["framework_id"], ["frameworks.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_artefacts_framework_id", "artefacts", ["framework_id"])
    op.create_index(
        "ix_artefacts_framework_id_ord", "artefacts", ["framework_id", "ord"]
    )

    op.create_table(
        "synced_vector_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("doc_id", sa.String(), nullable=False),
        sa.Column("vs_id", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("first_synced_at", sa.DateTime(), nullable=True),
        sa.Column("last_synced_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("doc_id", "vs_id", name="uix_doc_vs"),
    )
    op.create_index("ix_synced_vector_items_doc_id", "synced_vector_items", ["doc_id"])
    op.create_index("ix_synced_vector_items_vs_id", "synced_vector_items", ["vs_id"])

    op.create_table(
        "agent_runs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "status", sa.String(), server_default=sa.text("'pending'"), nullable=False
        ),
        sa.Column("model", sa.String(), nullable=True),
        sa.Column("selected_skill", sa.String(), nullable=True),
        sa.Column("skill_version", sa.String(), nullable=True),
        sa.Column(
            "allowed_tools_json", JSONB, server_default=JSONB_ARRAY, nullable=False
        ),
        sa.Column(
            "skill_input_json", JSONB, server_default=JSONB_OBJECT, nullable=False
        ),
        sa.Column(
            "skill_output_json", JSONB, server_default=JSONB_OBJECT, nullable=False
        ),
        sa.Column("started_at", sa.DateTime(), server_default=NOW),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column(
            "total_tokens_in", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column(
            "total_tokens_out",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "cost_micros", sa.BigInteger(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("error", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_runs_user_id", "agent_runs", ["user_id"])

    op.create_table(
        "agent_messages",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content_text", sa.Text(), nullable=True),
        sa.Column("content_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("tool_call_id", sa.String(), nullable=True),
        sa.Column("parent_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=NOW),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["agent_messages.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_messages_run_id", "agent_messages", ["run_id"])

    op.create_table(
        "agent_tool_invocations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("message_id", sa.String(), nullable=True),
        sa.Column("tool_name", sa.String(), nullable=False),
        sa.Column("tool_version", sa.String(), nullable=True),
        sa.Column("input_schema_version", sa.String(), nullable=True),
        sa.Column("output_schema_version", sa.String(), nullable=True),
        sa.Column("args_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("result_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column(
            "status", sa.String(), server_default=sa.text("'pending'"), nullable=False
        ),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["message_id"], ["agent_messages.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_agent_tool_invocations_run_id", "agent_tool_invocations", ["run_id"]
    )

    op.create_table(
        "documents",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=True),
        sa.Column("source_uri", sa.String(), nullable=True),
        sa.Column("hash", sa.String(), nullable=True),
        sa.Column("mime", sa.String(), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=True),
        sa.Column(
            "status", sa.String(), server_default=sa.text("'pending'"), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(), server_default=NOW),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_user_id", "documents", ["user_id"])
    op.create_index("ix_documents_hash", "documents", ["hash"])

    op.create_table(
        "document_chunks",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("document_id", sa.String(), nullable=False),
        sa.Column("ord", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "token_count", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("embedding", Vector(1024), nullable=True),
        sa.Column("embedding_model", sa.String(), nullable=True),
        sa.Column(
            "embedding_dim",
            sa.Integer(),
            server_default=sa.text("1024"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_document_chunks_document_id", "document_chunks", ["document_id"]
    )
    op.create_index(
        "ix_document_chunks_document_id_ord", "document_chunks", ["document_id", "ord"]
    )
    op.execute(
        "CREATE INDEX ix_document_chunks_embedding_hnsw "
        "ON document_chunks USING hnsw (embedding vector_cosine_ops)"
    )

    op.create_table(
        "citations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=True),
        sa.Column("message_id", sa.String(), nullable=True),
        sa.Column("document_id", sa.String(), nullable=True),
        sa.Column("chunk_id", sa.String(), nullable=True),
        sa.Column("framework_id", sa.String(), nullable=True),
        sa.Column("version", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["message_id"], ["agent_messages.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["chunk_id"], ["document_chunks.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["framework_id"], ["frameworks.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_citations_run_id", "citations", ["run_id"])
    op.create_index("ix_citations_document_id", "citations", ["document_id"])
    op.create_index("ix_citations_chunk_id", "citations", ["chunk_id"])
    op.create_index("ix_citations_framework_id", "citations", ["framework_id"])

    op.create_table(
        "wiki_builds",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "status", sa.String(), server_default=sa.text("'pending'"), nullable=False
        ),
        sa.Column("source_hash", sa.String(), nullable=True),
        sa.Column("started_at", sa.DateTime(), server_default=NOW),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("metrics_json", JSONB, server_default=JSONB_OBJECT, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_wiki_builds_user_id", "wiki_builds", ["user_id"])

    op.create_table(
        "wiki_pages",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column(
            "source_refs_json", JSONB, server_default=JSONB_ARRAY, nullable=False
        ),
        sa.Column(
            "version", sa.String(), server_default=sa.text("'1'"), nullable=False
        ),
        sa.Column("build_id", sa.String(), nullable=True),
        sa.Column(
            "status", sa.String(), server_default=sa.text("'draft'"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), server_default=NOW),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["build_id"], ["wiki_builds.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_wiki_pages_user_id", "wiki_pages", ["user_id"])
    op.create_index("ix_wiki_pages_slug", "wiki_pages", ["slug"])
    op.execute(
        "CREATE INDEX ix_wiki_pages_search ON wiki_pages USING gin "
        "(to_tsvector('english', coalesce(title, '') || ' ' || "
        "coalesce(summary, '') || ' ' || coalesce(body, '')))"
    )

    op.create_table(
        "wiki_claims",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("page_id", sa.String(), nullable=False),
        sa.Column("claim_text", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column(
            "source_chunk_ids_json", JSONB, server_default=JSONB_ARRAY, nullable=False
        ),
        sa.Column(
            "status", sa.String(), server_default=sa.text("'active'"), nullable=False
        ),
        sa.ForeignKeyConstraint(["page_id"], ["wiki_pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_wiki_claims_page_id", "wiki_claims", ["page_id"])
    op.execute(
        "CREATE INDEX ix_wiki_claims_search ON wiki_claims USING gin "
        "(to_tsvector('english', claim_text))"
    )

    op.create_table(
        "wiki_links",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("from_page_id", sa.String(), nullable=False),
        sa.Column("to_page_id", sa.String(), nullable=False),
        sa.Column("relation", sa.String(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["from_page_id"], ["wiki_pages.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["to_page_id"], ["wiki_pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_wiki_links_from_page_id", "wiki_links", ["from_page_id"])
    op.create_index("ix_wiki_links_to_page_id", "wiki_links", ["to_page_id"])

    op.create_table(
        "wiki_entities",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("canonical_page_id", sa.String(), nullable=True),
        sa.Column("aliases_json", JSONB, server_default=JSONB_ARRAY, nullable=False),
        sa.ForeignKeyConstraint(
            ["canonical_page_id"], ["wiki_pages.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_wiki_entities_name", "wiki_entities", ["name"])

    op.create_table(
        "wiki_eval_questions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("build_id", sa.String(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column(
            "expected_refs_json", JSONB, server_default=JSONB_ARRAY, nullable=False
        ),
        sa.Column(
            "last_result_json", JSONB, server_default=JSONB_OBJECT, nullable=False
        ),
        sa.ForeignKeyConstraint(["build_id"], ["wiki_builds.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_wiki_eval_questions_build_id", "wiki_eval_questions", ["build_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_wiki_eval_questions_build_id", table_name="wiki_eval_questions")
    op.drop_table("wiki_eval_questions")
    op.drop_index("ix_wiki_entities_name", table_name="wiki_entities")
    op.drop_table("wiki_entities")
    op.drop_index("ix_wiki_links_to_page_id", table_name="wiki_links")
    op.drop_index("ix_wiki_links_from_page_id", table_name="wiki_links")
    op.drop_table("wiki_links")
    op.execute("DROP INDEX IF EXISTS ix_wiki_claims_search")
    op.drop_index("ix_wiki_claims_page_id", table_name="wiki_claims")
    op.drop_table("wiki_claims")
    op.execute("DROP INDEX IF EXISTS ix_wiki_pages_search")
    op.drop_index("ix_wiki_pages_slug", table_name="wiki_pages")
    op.drop_index("ix_wiki_pages_user_id", table_name="wiki_pages")
    op.drop_table("wiki_pages")
    op.drop_index("ix_wiki_builds_user_id", table_name="wiki_builds")
    op.drop_table("wiki_builds")
    op.drop_index("ix_citations_framework_id", table_name="citations")
    op.drop_index("ix_citations_chunk_id", table_name="citations")
    op.drop_index("ix_citations_document_id", table_name="citations")
    op.drop_index("ix_citations_run_id", table_name="citations")
    op.drop_table("citations")
    op.execute("DROP INDEX IF EXISTS ix_document_chunks_embedding_hnsw")
    op.drop_index("ix_document_chunks_document_id_ord", table_name="document_chunks")
    op.drop_index("ix_document_chunks_document_id", table_name="document_chunks")
    op.drop_table("document_chunks")
    op.drop_index("ix_documents_hash", table_name="documents")
    op.drop_index("ix_documents_user_id", table_name="documents")
    op.drop_table("documents")
    op.drop_index(
        "ix_agent_tool_invocations_run_id", table_name="agent_tool_invocations"
    )
    op.drop_table("agent_tool_invocations")
    op.drop_index("ix_agent_messages_run_id", table_name="agent_messages")
    op.drop_table("agent_messages")
    op.drop_index("ix_agent_runs_user_id", table_name="agent_runs")
    op.drop_table("agent_runs")
    op.drop_index("ix_synced_vector_items_vs_id", table_name="synced_vector_items")
    op.drop_index("ix_synced_vector_items_doc_id", table_name="synced_vector_items")
    op.drop_table("synced_vector_items")
    op.drop_index("ix_artefacts_framework_id_ord", table_name="artefacts")
    op.drop_index("ix_artefacts_framework_id", table_name="artefacts")
    op.drop_table("artefacts")
    op.drop_index("ix_frameworks_created_at", table_name="frameworks")
    op.drop_index("ix_frameworks_creator_id", table_name="frameworks")
    op.drop_index("ix_frameworks_family", table_name="frameworks")
    op.drop_index("ix_frameworks_id", table_name="frameworks")
    op.drop_table("frameworks")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_materials_id", table_name="materials")
    op.drop_table("materials")

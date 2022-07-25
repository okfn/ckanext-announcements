"""Add Announcements Models

Revision ID: 95aed1f25344
Revises: None
Create Date: 2022-07-06 15:31:04.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "85aed1f25344"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "announcements",
        sa.Column("id", sa.UnicodeText, primary_key=True),
        sa.Column("timestamp", sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column("user_creator_id", sa.UnicodeText, nullable=False),
        sa.Column(
            "from_date",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "to_date",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("message", sa.UnicodeText, nullable=True),
        sa.Column(
            "status",
            sa.Enum("draft", "active", "deleted", name="announcements_status_enum"),
            nullable=False,
        ),
        sa.Column("extras", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade():
    op.drop_table("announcements")

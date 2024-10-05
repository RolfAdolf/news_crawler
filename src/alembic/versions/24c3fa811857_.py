from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "24c3fa811857"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("headline", sa.String(), nullable=False),
        sa.Column("photo", sa.String(), nullable=True),
        sa.Column("posted_at", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("headline", "posted_at", name="news_headline_posted_at_uniq"),
    )
    op.create_index(op.f("ix_news_posted_at"), "news", ["posted_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_news_posted_at"), table_name="news")
    op.drop_table("news")

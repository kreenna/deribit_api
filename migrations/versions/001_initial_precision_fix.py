import sqlalchemy as sa
from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Удаляем старую таблицу если есть
    op.drop_table("price_records", if_exists=True)

    # Создаем новую с Numeric
    op.create_table(
        "price_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("price", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("ix_price_records_ticker", "ticker"),
        sa.Index("ix_price_records_created_at", "created_at"),
        sa.Index("ix_ticker_created_at", "ticker", "created_at")
    )


def downgrade():
    op.drop_table("price_records")

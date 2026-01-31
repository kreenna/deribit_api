import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # создание таблицы
    op.create_table("price_records",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("ticker", sa.String(length=10), nullable=False),
                    sa.Column("price", sa.Numeric(precision=20, scale=8), nullable=False),
                    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                              nullable=True),
                    sa.PrimaryKeyConstraint("id")
                    )

    # индексы для производительности
    op.create_index(op.f("ix_price_records_ticker"), "price_records", ["ticker"], unique=False)
    op.create_index(op.f("ix_price_records_created_at"), "price_records", ["created_at"],
                    unique=False)
    op.create_index("ix_ticker_created_at", "price_records", ["ticker", "created_at"],
                    unique=False)


def downgrade():
    # удаление (для отката)
    op.drop_index(op.f("ix_price_records_ticker"), table_name="price_records")
    op.drop_index(op.f("ix_price_records_created_at"), table_name="price_records")
    op.drop_index("ix_ticker_created_at", table_name="price_records")
    op.drop_table("price_records")

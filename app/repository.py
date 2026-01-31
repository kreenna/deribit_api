from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import PriceRecord
from clients.deribit_client import IndexPrice


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_price(self, price: IndexPrice) -> None:
        """Сохраняет цену в БД."""
        record = PriceRecord(
            ticker=price.ticker,
            price=Decimal(str(price.price))  # Decimal для точности
        )
        self.db.add(record)
        self.db.flush()  # Не commit, для batch insert

    def get_all_by_ticker(self, ticker: str) -> List[PriceRecord]:
        """Все записи по тикеру."""
        return (
            self.db.query(PriceRecord)
            .filter(PriceRecord.ticker == ticker)
            .order_by(PriceRecord.created_at.asc())
            .all()
        )

    def get_latest_by_ticker(self, ticker: str) -> PriceRecord | None:
        """Последняя запись по тикеру."""
        return (
            self.db.query(PriceRecord)
            .filter(PriceRecord.ticker == ticker)
            .order_by(desc(PriceRecord.created_at))
            .first()
        )

    def get_by_ticker_and_date(
            self,
            ticker: str,
            start_date: datetime,
            end_date: Optional[datetime] = None
    ) -> List[PriceRecord]:
        """Записи по тикеру и периоду."""
        query = (
            self.db.query(PriceRecord)
            .filter(
                PriceRecord.ticker == ticker,
                PriceRecord.created_at >= start_date
            )
        )

        if end_date:
            query = query.filter(PriceRecord.created_at <= end_date)

        return query.order_by(PriceRecord.created_at.asc()).all()

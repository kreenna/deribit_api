from datetime import datetime
from typing import List, Optional, Type

from sqlalchemy.orm import Session

from clients.deribit_client import IndexPrice
from models import PriceRecord


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_price(self, price: IndexPrice):
        record = PriceRecord(ticker=price.ticker, price=price.price)
        self.db.add(record)

    def get_all_by_ticker(self, ticker: str) -> List[PriceRecord]:
        return self.db.query(PriceRecord).filter(PriceRecord.ticker == ticker).all()

    def get_latest_by_ticker(self, ticker: str):
        return self.db.query(PriceRecord).filter(PriceRecord.ticker == ticker).order_by(
            PriceRecord.timestamp.desc()).first()

    def get_by_ticker_and_date(self, ticker: str, start_date: datetime,
                               end_date: Optional[datetime] = None) -> list[Type[PriceRecord]]:
        query = self.db.query(PriceRecord).filter(PriceRecord.ticker == ticker,
                                                  PriceRecord.timestamp >= start_date)
        if end_date:
            query = query.filter(PriceRecord.timestamp <= end_date)
        return query.order_by(PriceRecord.timestamp).all()

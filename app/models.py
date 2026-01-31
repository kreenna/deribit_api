from sqlalchemy import Column, Integer, String, Float, DateTime, Numeric
from sqlalchemy.sql import func

from app.database import Base


class PriceRecord(Base):
    """Модель для записи цены на момент времени."""

    __tablename__ = "price_records"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, index=True)
    price = Column(Numeric(precision=20, scale=8), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

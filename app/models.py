from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base


class PriceRecord(Base):
    """Модель для записи цены на момент времени."""

    __tablename__ = "price_records"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, index=True)
    price = Column(Float, nullable=False, precision=10, scale=2)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

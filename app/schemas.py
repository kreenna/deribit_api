from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal


class PriceRecordSchema(BaseModel):
    ticker: str = Field(..., max_length=10)
    price: Decimal = Field(..., decimal_places=8)
    timestamp: int = Field(..., ge=0)  # UNIX timestamp

    class ConfigDict:
        from_attributes = True
        json_encoders = {
            Decimal: float  # Автоконвертация Decimal -> float для JSON
        }


class PriceListResponse(BaseModel):
    prices: List[PriceRecordSchema]
    count: int

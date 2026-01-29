from typing import List

from pydantic import BaseModel


class PriceRecordSchema(BaseModel):
    ticker: str
    price: float
    timestamp: int

    class Config:
        from_attributes = True


class PriceListResponse(BaseModel):
    prices: List[PriceRecordSchema]

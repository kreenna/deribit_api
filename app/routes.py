from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import PriceRepository
from app.schemas import PriceRecordSchema

# создание роутера с префиксом и тегами
router = APIRouter(
    prefix="",  # префикс добавляется в main.py
    tags=["prices"],
    responses={
        404: {"description": "No data for ticker or date range"},
        422: {"description": "Invalid date format"}
    }
)


@router.get(
    "/{ticker}",
    response_model=List[PriceRecordSchema],
    summary="Получить все цены по тикеру",
    description="Возвращает все сохраненные записи цен для указанного тикера"
)
def get_all_prices(
        ticker: str,
        db: Session = Depends(get_db)
):
    """
    Получение всех исторических данных по тикеру.
    - **ticker**: BTC_USD или ETH_USD (обязательный)
    """

    repo = PriceRepository(db)
    ticker_upper = ticker.upper()

    if ticker_upper not in ["BTC_USD", "ETH_USD"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported ticker. Use BTC_USD or ETH_USD"
        )

    records = repo.get_all_by_ticker(ticker_upper)

    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No price data found for {ticker_upper}"
        )

    return records


@router.get(
    "/{ticker}/latest",
    response_model=PriceRecordSchema,
    summary="Получить последнюю цену",
    description="Возвращает самую свежую цену для тикера"
)
def get_latest_price(
        ticker: str,
        db: Session = Depends(get_db)
):
    """
    Получение последней известной цены тикера.

    - **ticker**: BTC_USD или ETH_USD (обязательный)
    """

    repo = PriceRepository(db)
    ticker_upper = ticker.upper()

    if ticker_upper not in ["BTC_USD", "ETH_USD"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported ticker. Use BTC_USD or ETH_USD"
        )

    record = repo.get_latest_by_ticker(ticker_upper)

    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"No price data found for {ticker_upper}"
        )

    return record


@router.get(
    "/{ticker}/by-date",
    response_model=List[PriceRecordSchema],
    summary="Получить цены по периоду",
    description="Фильтрация цен по временному диапазону"
)
def get_prices_by_date(
        ticker: str,
        start_date: datetime = Query(
            ...,
            description="Начальная дата (ISO 8601, UTC)",
            example="2026-01-01T00:00:00Z"
        ),
        end_date: Optional[datetime] = Query(
            None,
            description="Конечная дата (ISO 8601, UTC)",
            example="2026-01-30T23:59:59Z"
        ),
        db: Session = Depends(get_db)
):
    """
    Получение цен за указанный период времени.

    - **ticker**: BTC_USD или ETH_USD (обязательный)
    - **start_date**: Начало периода (обязательный, ISO 8601)
    - **end_date**: Конец периода (опциональный)
    """

    repo = PriceRepository(db)
    ticker_upper = ticker.upper()

    if ticker_upper not in ["BTC_USD", "ETH_USD"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported ticker. Use BTC_USD or ETH_USD"
        )

    # если end_date не указан, используем текущее время
    if end_date is None:
        from datetime import datetime as dt
        end_date = dt.utcnow()

    records = repo.get_by_ticker_and_date(ticker_upper, start_date, end_date)

    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No price data found for {ticker_upper} in range {start_date} - {end_date}"
        )

    return records

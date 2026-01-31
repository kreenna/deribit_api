import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.repository import PriceRepository
from app.models import PriceRecord
from clients.deribit_client import IndexPrice
from decimal import Decimal


@pytest.fixture
def mock_db():
    """Мок сессии БД."""

    db = MagicMock(spec=Session)
    db.add = MagicMock()
    db.commit = MagicMock()
    db.flush = MagicMock()
    return db


@pytest.fixture
def mock_record():
    """Мок записи."""

    record = MagicMock(spec=PriceRecord)
    record.ticker = "BTC_USD"
    record.price = Decimal("95234.56789012")
    record.created_at = datetime.now()
    return record


def test_save_price(mock_db, mock_record):
    repo = PriceRepository(mock_db)
    price = IndexPrice("BTC_USD", 95234.56789012, 1706780000)

    repo.save_price(price)

    mock_db.add.assert_called_once()
    called_record = mock_db.add.call_args[0][0]
    assert called_record.ticker == "BTC_USD"
    assert called_record.price == Decimal("95234.56789012")


def test_get_latest_by_ticker(mock_db, mock_record):
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_record

    repo = PriceRepository(mock_db)
    result = repo.get_latest_by_ticker("BTC_USD")

    assert result == mock_record
    mock_db.query.assert_called()

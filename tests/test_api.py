from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAPIEndpoints:

    @patch("app.routes.PriceRepository")
    def test_get_all_prices(self, mock_repo):
        """Тест всех цен."""

        mock_records = [
            MagicMock(ticker="BTC_USD", price=95234.56, timestamp=1706780000),
            MagicMock(ticker="BTC_USD", price=95300.12, timestamp=1706780600)
        ]
        mock_repo.return_value.get_all_by_ticker.return_value = mock_records

        response = client.get("/api/v1/BTC_USD")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["ticker"] == "BTC_USD"

    @patch("app.routes.PriceRepository")
    def test_get_latest_price(self, mock_repo):
        """Тест последней цены."""

        mock_record = MagicMock(ticker="ETH_USD", price=3541.23, timestamp=1706781200)
        mock_repo.return_value.get_latest_by_ticker.return_value = mock_record

        response = client.get("/api/v1/ETH_USD/latest")
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == "3541.23"

    @patch("app.routes.PriceRepository")
    def test_get_prices_by_date(self, mock_repo):
        """Тест фильтра по дате."""

        mock_records = [MagicMock(ticker="BTC_USD", price=95250.0, timestamp=1706780000)]
        mock_repo.return_value.get_by_ticker_and_date.return_value = mock_records

        from datetime import datetime
        start = datetime(2026, 1, 31)

        response = client.get("/api/v1/BTC_USD/by-date", params={"start_date": start.isoformat()})
        assert response.status_code == 200

    def test_invalid_ticker(self):
        """Тест невалидного тикера."""

        response = client.get("/api/v1/INVALID")
        assert response.status_code == 400
        assert "Unsupported ticker" in response.json()["detail"]

    def test_no_data(self):
        """Тест пустых данных."""

        with patch("app.routes.PriceRepository.get_all_by_ticker", return_value=[]):
            response = client.get("/api/v1/BTC_USD")
            assert response.status_code == 404

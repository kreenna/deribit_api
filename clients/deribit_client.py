from dataclasses import dataclass
from datetime import datetime

import aiohttp


@dataclass
class IndexPrice:
    """Индекс цены."""

    ticker: str
    price: float
    timestamp: int


class DeribitClient:
    """Клиент на Deribit."""

    def __init__(self, base_url: str = "https://test.deribit.com/api/v2"):
        """Инициализация."""

        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        """Открытие схемы."""

        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие смены."""

        if self.session:
            await self.session.close()

    async def get_index_price(self, index_name: str) -> IndexPrice:
        """Получение index_price для указанного индекса."""

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "public/get_index_price",
            "params": {"index_name": index_name}
        }
        timeout = aiohttp.ClientTimeout(total=10)  # 10s timeout
        async with self.session.post(
                f"{self.base_url}/public/get_index_price",
                json=payload,
                timeout=timeout
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            if "error" in data:
                raise ValueError(f"API Error: {data["error"]}")
            return IndexPrice(
                ticker=index_name.upper(),
                price=float(data["result"]["index_price"]),
                timestamp=int(datetime.now().timestamp())
            )

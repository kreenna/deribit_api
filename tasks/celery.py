import asyncio
import logging
import os

from celery import Celery

from app.database import get_db
from app.repository import PriceRepository
from clients.deribit_client import DeribitClient

logger = logging.getLogger(__name__)

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("deribit_api")

# конфигурация
app.conf.update(
    broker_url=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    result_backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    timezone="UTC",
    beat_schedule={
        "fetch-prices": {
            "task": "tasks.celery.fetch_prices",
            "schedule": 60.0,
        },
    },
)

app.autodiscover_tasks(["tasks"])


@app.task(name="tasks.celery.fetch_prices", bind=True)
def fetch_prices(self):
    tickers = ["btc_usd", "eth_usd"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        async def _fetch():
            async with DeribitClient() as client:
                db = next(get_db())
                repo = PriceRepository(db)
                for ticker in tickers:
                    try:
                        price = await client.get_index_price(ticker)
                        logger.info(f"{price.ticker}: ${price.price}")
                        repo.save_price(price)
                        db.commit()
                    except Exception as e:
                        logger.error(f"{ticker}: {e}")
                        db.rollback()
                db.close()
    finally:
        loop.close()

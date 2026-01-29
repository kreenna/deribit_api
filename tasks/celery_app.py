from celery import Celery
from celery.schedules import crontab
import os
from clients.deribit_client import DeribitClient
from app.repository import PriceRepository
from app.database import get_db
import asyncio

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery("price_tracker")
app.conf.broker_url = redis_url
app.conf.result_backend = redis_url

app.conf.beat_schedule = {
    "fetch-prices-minute": {
        "task": "tasks.celery_app.fetch_prices",
        "schedule": crontab(minute="*"),
    },
}


@app.task(bind=True)
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
                        repo.save_price(price)
                        db.commit()
                    except Exception:
                        db.rollback()
                db.close()

        loop.run_until_complete(_fetch())
    finally:
        loop.close()

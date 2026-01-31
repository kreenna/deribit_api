from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app import routes

# создание таблиц при старте
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: инициализация (логирование, healthcheck)
    print("🚀 Deribit API started")
    print("📊 Endpoints: /prices/{ticker}, /prices/{ticker}/latest, /prices/{ticker}/by-date")
    print("📱 Docs: http://localhost:8000/docs")
    yield
    # shutdown
    print("🛑 API shutdown")


# инициализация FastAPI app
app = FastAPI(
    title="Deribit Price Tracker API",
    description="API для получения исторических index цен BTC_USD и ETH_USD с Deribit",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware для frontend интеграции
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключение роутеров
app.include_router(routes.router, prefix="/api/v1")


# healthcheck endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "deribit_api"}


@app.get("/")
def root():
    """Корневой endpoint с информацией."""
    return {
        "message": "Deribit Price Tracker API",
        "endpoints": [
            "/api/v1/prices/{ticker}",
            "/api/v1/prices/{ticker}/latest",
            "/api/v1/prices/{ticker}/by-date?start_date=...&end_date=..."
        ],
        "tickers": ["BTC_USD", "ETH_USD"],
        "docs": "/docs"
    }


# глобальный exception handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Ticker not found or no data available"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

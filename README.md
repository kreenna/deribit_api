# Deribit API 
Автоматический сбор и API цен BTC/ETH с Deribit каждую минуту.

---

## Функции

- ```Celery``` - собирает цены с Deribit API каждую минуту;
- ```PostgreSQL``` - хранит исторические данные;
- ```FastAPI REST``` - endpoints для данных;
- ```Swagger UI``` - интерактивная документация.

---

## Endpoints

- ```GET /api/v1/BTC_USD/latest``` - Последняя цена;
- ```GET /api/v1/BTC_USD``` - Все цены BTC;
- ```GET /api/v1/BTC_USD/by-date?start_date=...``` - Фильтр по дате;
- ```GET /docs```	- Swagger UI.

---

### Быстрый старт 

```
# клонировать + Docker
git clone https://gitlab.com/rudenskaaarina/deribit_api && cd deribit_api
docker-compose up --build

# ждем данные (2 мин)
sleep 120

# тест
curl "http://localhost:8000/api/v1/BTC_USD/latest"
Открыть: http://localhost:8000/docs
```

---

### Тестирование

```
pytest tests/ -v
```
---

### Пример ответов API

1. Последняя цена:

```
$ curl "http://localhost:8000/api/v1/BTC_USD/latest"
{
  "ticker": "BTC_USD",
  "price": 95234.56789012,
  "timestamp": 1706789000
}
```

2. Все цены (24+ записей):

```
$ curl "http://localhost:8000/api/v1/BTC_USD" | jq 'length'
24
```

3. За 24 часа:

```
$ curl "http://localhost:8000/api/v1/ETH_USD/by-date?start_date=2026-01-31T00:00:00Z" | jq
[...]
```

---

### Миграции Alembic

```
# статус
alembic current

# новая миграция (при изменении моделей)
alembic revision --autogenerate -m "add_field"

# применить
alembic upgrade head

# откат
alembic downgrade -1
```

---

# Учебный проект FastAPI

## Запуск

```powershell
uv sync
uv run uvicorn app.main:app --reload
```

Откройте http://127.0.0.1:8000/docs для Swagger UI.

Всё запускается из локального `.venv`; глобальные Python-пакеты не используются.

## Структура проекта

```text
app/
├── api/routes/       # HTTP-маршруты
├── repositories/     # Хранение и получение данных
├── schemas/          # Pydantic-модели запросов
├── services/         # Бизнес-логика
└── main.py           # Создание FastAPI-приложения
main.py               # Точка входа для импорта app
```

Сейчас кошельки хранятся в памяти и сбрасываются при перезапуске приложения.

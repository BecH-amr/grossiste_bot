# Telegram Catalog Bot - Review Memory

## Project: telegram_chine
- **Stack**: Python 3.12, aiogram 3.x, FastAPI, SQLModel, aiosqlite, pydantic-settings, loguru, uvicorn
- **Architecture**: FastAPI lifespan manages bot lifecycle; polling mode creates background task, webhook mode uses FastAPI endpoint
- **Database**: SQLite via aiosqlite, async sessions via SQLAlchemy/SQLModel
- **Key files**: app/main.py (entrypoint), app/bot/setup.py (bot/dispatcher), app/bot/handlers/ (start, catalog), app/models.py, app/crud.py

## Patterns Observed
- Default parse mode is MarkdownV2 (set in bot setup) -- all message text must be escaped
- Session management: `async_session_factory()` used directly in handlers (not via FastAPI DI)
- Callback data format: `"prefix:id"` pattern (cat:1, product:5)
- Manual MarkdownV2 escaping via regex in `app/utils/formatting.py`

## Common Issues Found (2026-03-08)
- **aiogram 3**: `call.message` can be None or InaccessibleMessage -- always guard before calling methods
- **aiogram 3**: CallbackData should be validated; raw `int()` on split data is crash-prone
- **SQLModel**: `datetime.utcnow` deprecated in Python 3.12+, use `datetime.now(timezone.utc)`
- **SQLAlchemy**: `sessionmaker` with `class_=AsyncSession` is legacy; use `async_sessionmaker`
- **Security**: Bot token in webhook URL path must never be logged
- **Lifecycle**: `asyncio.create_task()` for polling must store task ref and cancel on shutdown
- **MarkdownV2**: Incomplete escaping is a recurring pattern; any unescaped special char causes silent failures

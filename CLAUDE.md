# telegram_chine — Claude Code Rules

## Stack
- Python **3.12+** · aiogram **3.x** · FastAPI · SQLModel + SQLAlchemy **2.0** · aiosqlite · pydantic-settings 2.x
- Package manager: **uv** (`uv add`, `uv run`)
- DB: SQLite (aiosqlite) via `catalog.db`

## Commands
```bash
uv run python -m app.main           # start bot (polling dev mode)
uv run python -m scripts.seed_db   # populate DB
uv run python -c "import secrets; print(secrets.token_urlsafe(32))"  # gen SECRET_TOKEN
```

## Critical Rules

### Before writing any code — check latest docs
If using a library API you haven't verified in this session, **WebFetch the official docs first**:
- aiogram 3: https://docs.aiogram.dev/en/latest/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- FastAPI: https://fastapi.tiangolo.com/
- SQLModel: https://sqlmodel.tiangolo.com/

### Python 3.12+ — forbidden patterns
| NEVER use | Use instead |
|---|---|
| `Optional[X]` | `X \| None` |
| `datetime.utcnow()` | `datetime.now(timezone.utc)` |
| `List[X]`, `Dict[K,V]` from typing | `list[X]`, `dict[K,V]` |
| `sessionmaker(..., class_=AsyncSession)` | `async_sessionmaker(engine)` |
| `from sqlmodel.ext.asyncio.session import AsyncSession` | `from sqlalchemy.ext.asyncio import AsyncSession` |
| `session.exec(select(...))` | `session.execute(select(...))` + `.scalars().all()` |

### aiogram 3 — mandatory patterns
- All callback data: use `CallbackData` factory — **never** `call.data.split(":")[1]`
- Before any `call.message.method()`: guard with `if not isinstance(call.message, Message): return`
- Editing a photo message: delete + send new — never `edit_text()` on a photo message

### Security
- Token comparison: **always** `hmac.compare_digest()`, never `==`
- `SECRET_TOKEN` must be required (no default), never logged

### Async / shutdown
- `asyncio.create_task()`: always save the reference, always cancel + await on shutdown
- Always call `await engine.dispose()` in lifespan teardown

### Data
- Prices: `int` (whole EUR units), never `float`
- Seed scripts: check for existing data first (idempotent)
- After `session.add()` in bulk: use `await session.flush()` before referencing auto-generated IDs

## Architecture
```
app/core/        → config.py, database.py
app/models.py    → SQLModel tables
app/crud.py      → all DB queries
app/bot/
  setup.py       → Bot + Dispatcher singletons
  callbacks.py   → CallbackData classes
  keyboards.py   → keyboard builders
  handlers/      → start.py, catalog.py
app/utils/       → formatting.py (escape_md)
scripts/         → seed_db.py
```

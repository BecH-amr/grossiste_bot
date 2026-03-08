# Grossiste Bot

Catalog bot for wholesale product resale. Customers browse categories, view products with photos and prices, and reach out via Snapchat to order.

## Stack

- **aiogram 3.x** — Telegram bot framework
- **FastAPI + uvicorn** — web server (webhook mode in prod)
- **SQLModel + aiosqlite** — async SQLite ORM
- **pydantic-settings** — typed `.env` config
- **uv** — package manager

## Setup

```bash
# Install dependencies
uv sync

# Copy and fill in your config
cp .env.example .env
# Edit .env: set BOT_TOKEN, SECRET_TOKEN, CONTACT_SNAPCHAT

# Seed the database
uv run python -B -m scripts.seed_db

# Start the bot (polling mode)
uv run python -B -m app.main
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | Yes | From [@BotFather](https://t.me/BotFather) |
| `SECRET_TOKEN` | Yes | Random string — `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `CONTACT_SNAPCHAT` | Yes | Your Snapchat handle (e.g. `@your_snap`) |
| `DB_URL` | No | SQLite path (default: `sqlite+aiosqlite:///./catalog.db`) |
| `USE_POLLING` | No | `true` for local dev, `false` for webhook prod (default: `true`) |
| `WEBHOOK_URL` | Prod only | Your public domain (e.g. `https://yourapp.railway.app`) |

## Bot flow

```
/start
  └── Welcome + [Voir le Catalogue]  [Nous Contacter → Snapchat]

[Voir le Catalogue]
  └── Category list

[Category]
  └── Product list with prices

[Product]
  └── Photo + name + price + stock status
      [Retour]  [Commander → Snapchat]
```

## Adding product photos

1. Start the bot
2. Send any photo directly to the bot in Telegram
3. The bot replies with the `file_id`
4. Associate it with a product:

```bash
uv run python -B -m scripts.set_photo "Product name" "file_id_here"
```

## Project structure

```
app/
  core/         config.py, database.py
  bot/
    handlers/   start.py, catalog.py
    callbacks.py, keyboards.py, setup.py
  models.py     Category + Product SQLModel tables
  crud.py       DB queries
  utils/        formatting.py (escape_md, format_price)
scripts/
  seed_db.py    Populate DB with initial data
  set_photo.py  Assign a Telegram file_id to a product
```

## Deployment (Railway)

1. Push to GitHub
2. Create a new Railway project from the repo
3. Set all env variables (`BOT_TOKEN`, `SECRET_TOKEN`, `CONTACT_SNAPCHAT`, `USE_POLLING=false`, `WEBHOOK_URL=https://your-app.railway.app`)
4. Railway auto-deploys on push

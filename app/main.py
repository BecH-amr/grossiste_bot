import asyncio
import contextlib
import hmac
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Request
from loguru import logger
from sqlmodel import SQLModel

from app.bot.setup import bot, dp, register_handlers
from app.core.config import settings
from app.core.database import engine


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables ready")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    register_handlers()

    polling_task = None
    if settings.USE_POLLING:
        logger.info("Starting bot in polling mode")
        async def _poll() -> None:
            try:
                await dp.start_polling(bot)
            except Exception as e:
                logger.exception("Polling failed: {}", e)
                raise
        polling_task = asyncio.create_task(_poll())
    else:
        webhook_url = f"{settings.WEBHOOK_URL}/webhook/{settings.BOT_TOKEN}"
        await bot.set_webhook(webhook_url, secret_token=settings.SECRET_TOKEN)
        logger.info("Webhook configured")

    yield

    if polling_task is not None:
        polling_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await polling_task
    else:
        await bot.delete_webhook()

    await bot.session.close()
    await engine.dispose()
    logger.info("Bot shut down")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def healthcheck() -> dict:
    return {"ok": True}


@app.post("/webhook/{token}")
async def webhook(
    token: str,
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=""),
) -> dict:
    if not hmac.compare_digest(token, settings.BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not hmac.compare_digest(x_telegram_bot_api_secret_token, settings.SECRET_TOKEN):
        raise HTTPException(status_code=403, detail="Forbidden")

    from aiogram.types import Update
    try:
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.exception("Failed to process update: {}", e)
    return {"ok": True}


def main() -> None:
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()

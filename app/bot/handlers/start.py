from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from app.bot.keyboards import main_menu_keyboard

router = Router()

WELCOME = (
    "👋 Bienvenue chez *Grossiste Bot*\\!\n\n"
    "⚠️ *Minimum de commande par modèle* \\: voir chaque produit\\.\n\n"
    "Choisissez une option ci\\-dessous\\."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME, reply_markup=main_menu_keyboard())


@router.message(F.photo)
async def log_photo(message: Message) -> None:
    file_id = message.photo[-1].file_id
    logger.info(f"📸 file_id: {file_id}")
    await message.reply(f"`{file_id}`")

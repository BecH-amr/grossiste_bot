from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from app.bot.callbacks import CategoryCB, ProductCB
from app.bot.keyboards import categories_keyboard, product_keyboard, products_keyboard
from app.core.database import async_session_factory
from app.crud import get_categories, get_product_by_id, get_products_by_category
from app.utils.formatting import format_product_caption

router = Router()

MSG_INACCESSIBLE = "Message inaccessible."


async def _edit_or_replace(message: Message, text: str, **kwargs) -> None:
    """Edit text message in place, or delete+send if the message is a photo."""
    if message.photo:
        try:
            await message.delete()
        except TelegramBadRequest:
            pass
        await message.answer(text, **kwargs)
    else:
        try:
            await message.edit_text(text, **kwargs)
        except TelegramBadRequest:
            await message.answer(text, **kwargs)


@router.callback_query(lambda c: c.data == "show_categories")
async def cb_show_categories(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer(MSG_INACCESSIBLE, show_alert=True)
        return

    async with async_session_factory() as session:
        categories = await get_categories(session)

    if not categories:
        await call.answer("Aucune catégorie disponible pour l'instant.", show_alert=True)
        return

    await call.answer()
    await _edit_or_replace(call.message, "🗂️ *Choisissez une catégorie* \\:", reply_markup=categories_keyboard(categories))


@router.callback_query(CategoryCB.filter())
async def cb_show_products(call: CallbackQuery, callback_data: CategoryCB) -> None:
    if not isinstance(call.message, Message):
        await call.answer(MSG_INACCESSIBLE, show_alert=True)
        return

    async with async_session_factory() as session:
        products = await get_products_by_category(session, callback_data.id)

    if not products:
        await call.answer("Aucun produit dans cette catégorie.", show_alert=True)
        return

    await call.answer()
    await _edit_or_replace(call.message, "📦 *Choisissez un produit* \\:", reply_markup=products_keyboard(products))


@router.callback_query(ProductCB.filter())
async def cb_show_product(call: CallbackQuery, callback_data: ProductCB) -> None:
    if not isinstance(call.message, Message):
        await call.answer(MSG_INACCESSIBLE, show_alert=True)
        return

    async with async_session_factory() as session:
        product = await get_product_by_id(session, callback_data.id)

    if not product:
        await call.answer("Produit introuvable.", show_alert=True)
        return

    await call.answer()
    caption = format_product_caption(product)
    keyboard = product_keyboard(product)

    if product.photo_file_id:
        await call.message.answer_photo(
            photo=product.photo_file_id,
            caption=caption,
            reply_markup=keyboard,
        )
        try:
            await call.message.delete()
        except TelegramBadRequest:
            pass
    else:
        try:
            await call.message.edit_text(caption, reply_markup=keyboard)
        except TelegramBadRequest:
            await call.message.answer(caption, reply_markup=keyboard)

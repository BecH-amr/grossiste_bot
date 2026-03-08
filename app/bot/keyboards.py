from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks import CategoryCB, ProductCB
from app.core.config import settings
from app.models import Category, Product
from app.utils.formatting import format_price


def _snapchat_url() -> str:
    username = settings.CONTACT_SNAPCHAT.lstrip("@")
    return f"https://snapchat.com/add/{username}"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍️ Voir le Catalogue", callback_data="show_categories")],
        [InlineKeyboardButton(text="📞 Nous Contacter", url=_snapchat_url())],
    ])


def categories_keyboard(categories: list[Category]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text=f"{cat.emoji} {cat.name}",
            callback_data=CategoryCB(id=cat.id).pack(),
        )]
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_keyboard(products: list[Product]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text=f"{p.name} — {format_price(p.price)}" + ("" if p.in_stock else " ❌"),
            callback_data=ProductCB(id=p.id).pack(),
        )]
        for p in products
    ]
    buttons.append([InlineKeyboardButton(text="⬅️ Catégories", callback_data="show_categories")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_keyboard(product: Product) -> InlineKeyboardMarkup:
    row = [InlineKeyboardButton(text="⬅️ Retour", callback_data=CategoryCB(id=product.category_id).pack())]
    if product.in_stock:
        row.append(InlineKeyboardButton(text="📩 Commander", url=_snapchat_url()))
    return InlineKeyboardMarkup(inline_keyboard=[row])

import re

from app.models import Product


def escape_md(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!\\])", r"\\\1", str(text))


def format_price(price_cents: int) -> str:
    """Convert centimes to display string. 850 → '8,50 €'"""
    euros = price_cents // 100
    cents = price_cents % 100
    if cents:
        return f"{euros},{cents:02d} €"
    return f"{euros} €"


def format_product_caption(product: Product) -> str:
    stock = escape_md("✅ En stock" if product.in_stock else "❌ Rupture de stock")
    lines = [
        f"*{escape_md(product.name)}*",
        f"💰 {escape_md(format_price(product.price))}  \\|  {stock}",
    ]
    if product.description:
        lines.append(f"\n_{escape_md(product.description)}_")
    return "\n".join(lines)

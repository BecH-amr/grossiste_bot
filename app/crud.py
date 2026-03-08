from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Category, Product


async def get_categories(session: AsyncSession) -> list[Category]:
    result = await session.execute(select(Category).order_by(Category.sort_order))
    return list(result.scalars().all())


async def get_products_by_category(session: AsyncSession, category_id: int) -> list[Product]:
    result = await session.execute(
        select(Product)
        .where(Product.category_id == category_id)
        .order_by(Product.name)
    )
    return list(result.scalars().all())


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)

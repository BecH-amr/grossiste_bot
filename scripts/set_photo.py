"""
Usage: uv run python -B -m scripts.set_photo "Nom du produit" "file_id"
"""
import asyncio
import sys

from sqlmodel import select

from app.core.database import async_session_factory, engine
from app.models import Product
from sqlmodel import SQLModel


async def main(name: str, file_id: str) -> None:
    async with async_session_factory() as session:
        result = await session.execute(select(Product).where(Product.name == name))
        product = result.scalars().first()
        if not product:
            print(f"Produit introuvable: {name!r}")
            return
        product.photo_file_id = file_id
        await session.commit()
        print(f"OK: {product.name}")

    await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: uv run python -B -m scripts.set_photo "Nom du produit" "file_id"')
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))

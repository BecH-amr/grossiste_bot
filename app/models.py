from datetime import datetime, timezone

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    emoji: str = ""
    sort_order: int = 0

    products: list["Product"] = Relationship(back_populates="category")


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    price: int  # centimes (850 = 8,50 EUR)
    currency: str = "EUR"
    photo_file_id: str | None = None
    in_stock: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    category_id: int = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="products")

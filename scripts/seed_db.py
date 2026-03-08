"""
Run with: uv run python scripts/seed_db.py
Prices stored in centimes (850 = 8,50 €)
"""
import asyncio

from sqlmodel import SQLModel, select

from app.core.database import engine, async_session_factory
from app.models import Category, Product


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_factory() as session:
        existing = await session.execute(select(Category))
        if existing.scalars().first():
            print("Database already seeded. Skipping.")
            return

        categories = [
            Category(name="Apple Audio", emoji="🎧", sort_order=1),
            Category(name="Apple Watch", emoji="⌚", sort_order=2),
            Category(name="Accessoires Apple", emoji="🔌", sort_order=3),
            Category(name="Gaming", emoji="🎮", sort_order=4),
            Category(name="Maillots de Foot", emoji="⚽", sort_order=5),
            Category(name="Mode & Vêtements", emoji="👗", sort_order=6),
        ]
        for cat in categories:
            session.add(cat)
        await session.flush()

        audio, watch, accessoires, gaming, foot, mode = categories

        MIN_30 = "Min. 30 pcs/modèle."
        MIN_50_FOOT = "Min. 50 maillots total · 10 pcs/équipe · max 5 équipes."
        MIN_50_SXL = "Envoi compris. Tailles S–XL. Min. 50 pcs · 10 pcs/couleur."
        MIN_50_M3XL = "Tailles M–3XL. Min. 50 pcs · 10 pcs/couleur."

        products = [
            # ── Apple Audio ──────────────────────────────────────────────
            Product(
                name="AirPods Pro 2",
                description=f"Réduction de bruit active, son premium. {MIN_30}",
                price=850,
                category_id=audio.id,
            ),
            Product(
                name="AirPods 3",
                description="Son spatial, résistant à l'eau. Min. 30 pcs/modèle.",
                price=1150,
                category_id=audio.id,
            ),
            Product(
                name="AirPods 4",
                description="Nouvelle génération, design amélioré. Min. 30 pcs/modèle.",
                price=1300,
                category_id=audio.id,
            ),
            Product(
                name="AirPods Max",
                description="Casque over-ear Apple. Min. 30 pcs/modèle.",
                price=2500,
                category_id=audio.id,
            ),
            Product(
                name="AirPods Max Premium",
                description="Finitions haut de gamme, qualité supérieure. Min. 30 pcs/modèle.",
                price=8000,
                category_id=audio.id,
            ),

            # ── Apple Watch ───────────────────────────────────────────────
            Product(
                name="Apple Watch Ultra 2 — Bluetooth",
                description="Sans SIM, connectivité Bluetooth. Min. 30 pcs/modèle.",
                price=2350,
                category_id=watch.id,
            ),
            Product(
                name="Apple Watch Ultra 2 — Caméra + SIM",
                description="Caméra première qualité + SIM intégrée. Min. 30 pcs/modèle.",
                price=4700,
                category_id=watch.id,
            ),

            # ── Accessoires Apple ─────────────────────────────────────────
            Product(
                name="Câble USB-C vers USB-C",
                description="Charge rapide, compatible tous appareils USB-C. Min. 30 pcs/modèle.",
                price=300,
                category_id=accessoires.id,
            ),
            Product(
                name="Câble USB-C vers Lightning",
                description="Compatible iPhone, charge rapide. Min. 30 pcs/modèle.",
                price=250,
                category_id=accessoires.id,
            ),
            Product(
                name="Bloc Charge Rapide Apple 20W",
                description="Charge rapide 20W, format compact. Min. 30 pcs/modèle.",
                price=400,
                category_id=accessoires.id,
            ),
            Product(
                name="Batterie Portable Apple 5000 mAh",
                description="Compatible MagSafe, charge sans fil. Min. 30 pcs/modèle.",
                price=850,
                category_id=accessoires.id,
            ),

            # ── Gaming ────────────────────────────────────────────────────
            Product(
                name="PSP Multi Jeux",
                description="Console portable avec plusieurs jeux inclus. Min. 30 pcs/modèle.",
                price=3100,
                category_id=gaming.id,
            ),
            Product(
                name="Game Boy",
                description="Console rétro, jeux classiques. Min. 30 pcs/modèle.",
                price=3600,
                category_id=gaming.id,
            ),

            # ── Maillots de Foot ──────────────────────────────────────────
            Product(
                name="Maillot de Foot — Modèle Player",
                description=MIN_50_FOOT,
                price=1100,
                category_id=foot.id,
            ),
            Product(
                name="Maillot de Foot — Modèle Fan",
                description=MIN_50_FOOT,
                price=1100,
                category_id=foot.id,
            ),

            # ── Mode & Vêtements ──────────────────────────────────────────
            Product(
                name="Alo Yoga — Brassière + Leggings",
                description=MIN_50_SXL,
                price=2300,
                category_id=mode.id,
            ),
            Product(
                name="Alo Yoga — Brassière + Shorts",
                description=MIN_50_SXL,
                price=1800,
                category_id=mode.id,
            ),
            Product(
                name="Alo Yoga — Brassière + Leggings (modèle 2)",
                description=MIN_50_SXL,
                price=1900,
                category_id=mode.id,
            ),
            Product(
                name="Nike — T-shirt + Short",
                description="Tailles M–3XL. Min. 50 pcs · 10 pcs/couleur.",
                price=1600,
                category_id=mode.id,
            ),
            Product(
                name="Nike — T-shirt + Pantalon",
                description="Tailles M–3XL. Min. 50 pcs · 10 pcs/couleur.",
                price=1750,
                category_id=mode.id,
            ),
            Product(
                name="Pyjama Victoria's Secret",
                description="Tailles S–XL. Min. 50 pcs · 10 pcs/couleur.",
                price=2200,
                category_id=mode.id,
            ),
        ]

        for product in products:
            session.add(product)
        await session.commit()

    print(f"✅ {len(categories)} catégories · {len(products)} produits ajoutés.")
    print("Tip: envoie une photo à ton bot et note le file_id dans les logs pour l'ajouter aux produits.")


if __name__ == "__main__":
    asyncio.run(seed())

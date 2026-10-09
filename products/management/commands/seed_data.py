"""Load the initial HERLEZZ catalog and its product-specific benefits."""
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from products.models import Product, ProductBenefit


AUDIO_BENEFITS = (
    (ProductBenefit.Icon.AUDIO, "Sonido envolvente 3D espacial"),
    (ProductBenefit.Icon.CONNECTION, "Conexión instantánea magnética"),
    (ProductBenefit.Icon.NOISE, "Cancelación activa de ruido"),
    (ProductBenefit.Icon.WARRANTY, "Garantía oficial de 2 meses y cambio directo"),
)

WALLET_BENEFITS = (
    (ProductBenefit.Icon.MAGSAFE, "Se adhiere al teléfono con MagSafe"),
    (ProductBenefit.Icon.DESIGN, "Diseño elegante y minimalista"),
    (ProductBenefit.Icon.WARRANTY, "Garantía oficial de 2 meses y cambio directo"),
)

PRODUCTS = (
    {
        "slug": "airpods-2-gen",
        "name": "AirPods 2 Gen",
        "description": "Audio inalámbrico con sonido envolvente, conexión instantánea y cancelación activa de ruido.",
        "price": Decimal("20.00"),
        "badge_text": "CALIDAD PREMIUM",
        "includes_case": False,
        "source_image": "AC89C5B2-1221-4E72-8B0A-4E00FBD2015E.PNG",
        "image_name": "airpods-2-gen.png",
        "benefits": AUDIO_BENEFITS,
    },
    {
        "slug": "airpods-4",
        "name": "AirPods 4",
        "description": "Audio inalámbrico con sonido envolvente, conexión instantánea y cancelación activa de ruido.",
        "price": Decimal("25.00"),
        "badge_text": "CALIDAD PREMIUM",
        "includes_case": False,
        "source_image": "042036A3-30E8-46B9-AF9A-59E5DB799B3F.PNG",
        "image_name": "airpods-4.png",
        "benefits": AUDIO_BENEFITS,
    },
    {
        "slug": "airpods-max",
        "name": "AirPods Max",
        "description": "Audio de diadema con sonido envolvente y cancelación activa de ruido pro.",
        "price": Decimal("30.00"),
        "badge_text": "CALIDAD PREMIUM",
        "includes_case": False,
        "source_image": "1B8E5B09-A134-4686-9568-E33F8C748CEC.PNG",
        "image_name": "airpods-max.png",
        "benefits": AUDIO_BENEFITS,
    },
    {
        "slug": "combo-emprendedor",
        "name": "Combo Emprendedor",
        "description": "3 AirPods Pro 2 + 3 estuches protectores.",
        "price": Decimal("50.00"),
        "badge_text": "COMBO EMPRENDEDOR",
        "includes_case": True,
        "source_image": None,
        "image_name": None,
        "benefits": AUDIO_BENEFITS,
    },
    {
        "slug": "combo-super-mayorista",
        "name": "Combo Súper Mayorista",
        "description": "6 AirPods Pro 2 + 6 estuches protectores.",
        "price": Decimal("89.00"),
        "badge_text": "MAYORISTA",
        "includes_case": True,
        "source_image": None,
        "image_name": None,
        "benefits": AUDIO_BENEFITS,
    },
    {
        "slug": "billetera-magsafe",
        "name": "Billetera MagSafe",
        "description": "Se adhiere al teléfono con MagSafe. Diseño elegante y minimalista.",
        "price": Decimal("6.00"),
        "badge_text": "CALIDAD PREMIUM",
        "includes_case": False,
        "source_image": "DE94CA27-6BA4-439C-ABAA-ED9FF64215A9.PNG",
        "image_name": "billetera-magsafe.png",
        "benefits": WALLET_BENEFITS,
    },
)


class Command(BaseCommand):
    help = "Carga los seis productos de prueba y sus beneficios sin duplicarlos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-dir",
            type=Path,
            default=settings.BASE_DIR / "productosimagenes",
            help="Carpeta de los cuatro artes oficiales disponibles.",
        )

    def handle(self, *args, **options):
        source_dir = options["source_dir"]
        missing = [
            item["source_image"]
            for item in PRODUCTS
            if item["source_image"] and not (source_dir / item["source_image"]).is_file()
        ]
        if missing:
            raise CommandError(f"Faltan imágenes en {source_dir}: {', '.join(missing)}")

        created_count = 0
        benefit_count = 0
        for item in PRODUCTS:
            defaults = {
                key: item[key]
                for key in ("name", "description", "price", "badge_text", "includes_case")
            }
            product, created = Product.objects.get_or_create(
                slug=item["slug"], defaults=defaults
            )
            created_count += int(created)

            if item["source_image"] and (
                not product.image or not product.image.storage.exists(product.image.name)
            ):
                with (source_dir / item["source_image"]).open("rb") as source_file:
                    product.image.save(item["image_name"], File(source_file), save=True)

            for position, (icon, label) in enumerate(item["benefits"], start=1):
                _, benefit_created = ProductBenefit.objects.get_or_create(
                    product=product,
                    icon=icon,
                    defaults={"text": label, "position": position},
                )
                benefit_count += int(benefit_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo listo: {created_count} productos y {benefit_count} beneficios nuevos; "
                f"{len(PRODUCTS)} productos de prueba disponibles."
            )
        )

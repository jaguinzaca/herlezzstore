from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from .utils import build_whatsapp_url


class Product(models.Model):
    name = models.CharField("nombre", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True)
    description = models.TextField("descripción", blank=True)
    price = models.DecimalField(
        "precio",
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    image = models.ImageField("imagen", upload_to="products/", blank=True)
    is_active = models.BooleanField("activo", default=True)
    badge_text = models.CharField("etiqueta", max_length=60, blank=True)
    includes_case = models.BooleanField("incluye estuche", default=False)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["created_at", "pk"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.name

    @property
    def whatsapp_url(self):
        message = (
            "Hola, HERLEZZ. Quiero realizar un pedido:\n"
            f"Producto: {self.name}\n"
            f"Precio: ${self.price:.2f}\n"
            "¿Está disponible?"
        )
        return build_whatsapp_url(message)


class ProductBenefit(models.Model):
    class Icon(models.TextChoices):
        AUDIO = "audio", "Audio"
        CONNECTION = "connection", "Conexión"
        NOISE = "noise", "Cancelación de ruido"
        WARRANTY = "warranty", "Garantía"
        MAGSAFE = "magsafe", "MagSafe"
        DESIGN = "design", "Diseño"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="benefits",
        verbose_name="producto",
    )
    icon = models.CharField("icono", max_length=16, choices=Icon.choices)
    text = models.CharField("beneficio", max_length=160)
    position = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        ordering = ["position", "pk"]
        verbose_name = "beneficio"
        verbose_name_plural = "beneficios"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "icon"], name="unique_product_benefit_icon"
            )
        ]

    def __str__(self):
        return f"{self.product.name}: {self.text}"

from decimal import Decimal
from io import StringIO
import re
from urllib.parse import parse_qs, urlsplit

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.test.utils import override_settings

from .models import Product, ProductBenefit


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.active_product = Product.objects.create(
            name="Auriculares de prueba",
            slug="auriculares-de-prueba",
            price=Decimal("20.00"),
            image="products/auriculares.png",
            is_active=True,
        )
        Product.objects.create(
            name="Producto oculto",
            slug="producto-oculto",
            price=Decimal("30.00"),
            image="products/oculto.png",
            is_active=False,
        )

    def test_catalog_only_shows_active_products(self):
        response = self.client.get("/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auriculares de prueba")
        self.assertNotContains(response, "Producto oculto")
        self.assertContains(response, "Pedir por WhatsApp", count=1)
        self.assertContains(response, 'src="/static/products/herlezz.png"')
        self.assertNotIn("{%", html)
        self.assertNotIn("{{", html)
        self.assertIn("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8", html)

    def test_catalog_orders_active_products_by_price(self):
        Product.objects.create(
            name="Producto económico",
            slug="producto-economico",
            price=Decimal("5.00"),
            is_active=True,
        )

        response = self.client.get("/")

        self.assertEqual(
            list(response.context["products"].values_list("price", flat=True)),
            [Decimal("5.00"), Decimal("20.00")],
        )

    def test_catalog_has_a_clear_empty_state(self):
        Product.objects.all().delete()

        response = self.client.get("/")

        self.assertContains(response, "Pronto tendremos novedades.")
        self.assertNotContains(response, "Pedir por WhatsApp")

    def test_whatsapp_link_contains_selected_product_and_price(self):
        link = urlsplit(self.active_product.whatsapp_url)
        message = parse_qs(link.query)["text"][0]

        self.assertEqual(link.netloc, "wa.me")
        self.assertEqual(link.path, "/593983670320")
        self.assertIn("Auriculares de prueba", message)
        self.assertIn("$20.00", message)

    def test_wholesale_link_contains_the_requested_message(self):
        response = self.client.get("/")
        match = re.search(
            r'href="(https://wa\.me/593983670320\?text=[^"]+)"[^>]*>Contactar a Ventas Mayoristas',
            response.content.decode(),
        )
        self.assertIsNotNone(match)
        link = urlsplit(match.group(1))

        self.assertContains(response, "¿ERES MAYORISTA O QUIERES EMPRENDER?")
        self.assertContains(response, "Contactar a Ventas Mayoristas")
        self.assertEqual(link.path, "/593983670320")
        self.assertEqual(
            parse_qs(link.query)["text"][0],
            "¡Hola HERLEZZ! 👋 Estoy interesado en comprar al por mayor y quiero conocer "
            "la lista de precios mayorista, stock disponible y condiciones de envío.",
        )

    def test_card_renders_its_own_benefits_and_case_indicator(self):
        ProductBenefit.objects.create(
            product=self.active_product,
            icon=ProductBenefit.Icon.AUDIO,
            text="Sonido envolvente 3D espacial",
            position=1,
        )
        self.active_product.includes_case = True
        self.active_product.save(update_fields=["includes_case"])

        response = self.client.get("/")

        self.assertContains(response, "Sonido envolvente 3D espacial")
        self.assertContains(response, "Incluye estuche protector")
        self.assertContains(response, "$20.00")


class DevAdminCommandTests(TestCase):
    @override_settings(DEBUG=True)
    def test_creates_superuser_once(self):
        call_command("ensure_dev_admin", stdout=StringIO())
        call_command("ensure_dev_admin", stdout=StringIO())

        users = get_user_model().objects.filter(username="admin")
        self.assertEqual(users.count(), 1)
        self.assertTrue(users.first().is_superuser)
        self.assertTrue(users.first().check_password("admin12345"))

    @override_settings(DEBUG=False)
    def test_rejects_non_development_environment(self):
        with self.assertRaises(CommandError):
            call_command("ensure_dev_admin", stdout=StringIO())

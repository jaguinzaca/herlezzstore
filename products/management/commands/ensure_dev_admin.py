"""Create the explicitly requested local development superuser once."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea el superusuario admin para desarrollo local si aún no existe."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Este comando solo se permite con DJANGO_DEBUG=True.")

        user_model = get_user_model()
        existing = user_model.objects.filter(username="admin").first()
        if existing:
            if not existing.is_superuser or not existing.is_staff:
                raise CommandError(
                    "Ya existe 'admin' sin permisos de superusuario; revísalo manualmente."
                )
            self.stdout.write("El superusuario 'admin' ya existe; no se cambió su contraseña.")
            return

        user_model.objects.create_superuser(
            username="admin",
            email="admin@herlezz.com",
            password="admin12345",
        )
        self.stdout.write(self.style.SUCCESS("Superusuario local 'admin' creado."))

from urllib.parse import quote

from django.conf import settings


def build_whatsapp_url(message):
    return f"https://wa.me/{settings.HERLEZZ_WHATSAPP_NUMBER}?text={quote(message, safe='')}"

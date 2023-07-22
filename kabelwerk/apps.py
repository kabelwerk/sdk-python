"""
If you are using the Kabelwerk SDK for Python in a Django project, you can add
'kabelwerk' to your INSTALLED_APPS — and the relevant KABELWERK_* settings will
be picked up by the SDK.

This module assumes that you have Django installed. Do not import it directly.
"""

from django.apps import AppConfig
from django.conf import settings

from . import config


class KabelwerkAppConfig(AppConfig):
    name = 'kabelwerk'

    def ready(self):
        """
        Update the Kabelwerk config from the Django settings.
        """
        if hasattr(settings, 'KABELWERK_URL'):
            config.KABELWERK_URL = settings.KABELWERK_URL

        if hasattr(settings, 'KABELWERK_API_TOKEN'):
            config.KABELWERK_API_TOKEN = settings.KABELWERK_API_TOKEN

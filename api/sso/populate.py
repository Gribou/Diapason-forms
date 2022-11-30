from constance import config

from .models import SSOConfig


def populate():
    if config.KEYCLOAK_ENABLED:
        if not SSOConfig.objects.exists():
            SSOConfig.objects.create()

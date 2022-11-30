from django.core.management.base import BaseCommand

from sso.tasks import refresh_keycloak


class Command(BaseCommand):
    help = "Refresh keycloak config and user permissions from provider"

    def handle(self, *args, **options):
        refresh_keycloak.delay()

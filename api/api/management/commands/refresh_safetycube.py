from weakref import ref
from django.core.management.base import BaseCommand

from efneproject.celery import refresh_safetycube


class Command(BaseCommand):
    help = "Refresh status for all forms saved to SafetyCube"

    def handle(self, *args, **options):
        refresh_safetycube.delay()

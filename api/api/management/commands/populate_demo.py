from django.core.management.base import BaseCommand

from shared.populate import populate as populate_shared
from efne.populate import populate as populate_efne
from similitude.populate import populate as populate_simi
from brouillage.populate import populate as populate_brouillage
from custom import populate as populate_custom
from sso.populate import populate as populate_sso


class Command(BaseCommand):
    help = 'Populate database with objects for demo'

    def handle(self, *args, **options):
        populate_shared.populate_demo()
        populate_efne.populate_demo()
        populate_simi.populate_demo()
        populate_brouillage.populate_demo()
        populate_custom.populate()
        populate_sso()

from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = 'Pauses execution until database is available'

    def handle(self, *args, **options):
        """Handle the command"""
        try:
            self.stdout.write('Waiting for database...')
            db_conn = None
            while not db_conn:
                try:
                    db_conn = connections[DEFAULT_DB_ALIAS]
                except OperationalError:
                    self.stdout.write(
                        'Database unavailable, waiting 1 second...')
                    time.sleep(0.1)

            self.stdout.write(self.style.SUCCESS('Database available!'))
        except Exception as e:
            raise CommandError(e)

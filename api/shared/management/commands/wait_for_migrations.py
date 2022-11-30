from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.loader import MigrationLoader
import time

# Commande permettant d'attendre que la base de données soient migrée
# Utilisée par exemple dans scripts/entrypoint.sh


class Command(BaseCommand):
    help = 'Pauses execution until database is migrated'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Waiting for migration...')
            connection = connections[DEFAULT_DB_ALIAS]
            loader = MigrationLoader(connection)
            existing_migrations_count = len(loader.graph.nodes)
            while True:
                # loader needs to be recreated for count to be updated
                loader = MigrationLoader(connection)
                remaining = existing_migrations_count - len(
                    loader.applied_migrations.keys())
                if remaining <= 0:
                    break
                self.stdout.write(
                    '{} migrations remaining, waiting 1 second...'.format(remaining))
                time.sleep(0.1)
            self.stdout.write(self.style.SUCCESS('Database migrated!'))
        except Exception as e:
            raise CommandError(e)

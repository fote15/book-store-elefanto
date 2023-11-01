"""
Django command wait for the database to be available
"""
import time

from psycopg2 import OperationalError as PsycopgError
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command wait for db"""

    def handle(self, *args, **options):
        self.stdout.write('waiting for db...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from pathlib import Path
import shutil
import os


class Command(BaseCommand):
    help = 'Reset the database with default tables and data'
    
    def handle(self, *args, **options):
        db_loc = Path(settings.BASE_DIR).joinpath('db.sqlite3')
        if db_loc.exists():
            os.remove(db_loc.resolve())

        migration_loc = Path(settings.BASE_DIR).joinpath('ravnica/migrations')
        if migration_loc.exists():
            shutil.rmtree(migration_loc.resolve())
            
        os.environ['DJANGO_SUPERUSER_USERNAME'] = 'admin'
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'drumstix38'

        call_command('makemigrations', 'ravnica')
        call_command('migrate')
        call_command('loaddata', 'guilds')
        call_command('createsuperuser', '--noinput', '--email=fakeemail@fake.fake')
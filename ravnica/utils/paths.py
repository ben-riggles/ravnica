from django.conf import settings
from pathlib import Path


class Paths:
    BASE_DIR = Path(settings.BASE_DIR)
    CORE_DIR = BASE_DIR.joinpath('core')
    DECK_DIR = BASE_DIR.joinpath('decks')
    APP_DIR = BASE_DIR.joinpath('ravnica')
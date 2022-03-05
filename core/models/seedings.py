from typing import Dict
from django.apps import apps

from core.models import Record


class SeedingError(Exception):
    pass


class Seedings:
    def __init__(self, season:'Season' = None):
        seasonModel = apps.get_model('ravnica', 'Season')
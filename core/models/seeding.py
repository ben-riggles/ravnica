from typing import Dict
from django.apps import apps

from core.models import Record


class SeedingError(Exception):
    pass


class Seeding:
    def __init__(self, season:'Season' = None):
        self._order = list(apps.get_model('ravnica', 'Guild').objects.order_by('name').all())
        return
        if season is None:
            matches = apps.get_model('ravnica', 'Match').objects.all()
        else:
            matches = season.match_set.all()

        if not matches:
            self._order = list(apps.get_model('ravnica', 'Guild').objects.order_by('name').all())

    def __getitem__(self, idx:int) -> 'Guild':
        if idx < 1 or idx > 10:
            raise SeedingError('Index must be between 1 and 10')
        return self._order[idx-1]
        
    def __str__(self):
        return str(self._order)

    def __repr__(self):
        return f'Seeding({", ".join([str(x) for x in self._order])})'
from typing import Dict
from django.apps import apps

from core.models import Record


class SeedingError(Exception):
    pass


class Seeding:
    def __init__(self, season:'Season' = None):
        self.season = season
        self._order = self._load_data()

    def __getitem__(self, idx:int) -> 'Guild':
        if idx < 1 or idx > 10:
            raise SeedingError('Index must be between 1 and 10')
        return self._order[idx-1]
        
    def __str__(self):
        return str(self._order)

    def __repr__(self):
        return f'Seeding({", ".join([str(x) for x in self._order])})'

    def seedOf(self, guild:'Guild') -> int:
        return self._order.index(guild) + 1

    def _load_data(self):
        if self.season is None:
            return list(apps.get_model('ravnica', 'Guild').objects.order_by('name').all())

        if not self.season.completed():
            return self.season.standings[:]

        playoffs = self.season.playoffs
        standings = self.season.standings
        return playoffs[:] + standings[4:]

from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from ravnica.models import Season

from ravnica.models import Guild


class Seeding:
    def __init__(self, season: Season = None):
        self.season: Season = season
        self._data: List[Guild] = self._load_data()
        
    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        if self.season is None:
            return 'Seeding()'
        return f'Seeding(season={self.season.id})'

    def __getitem__(self, idx: int | slice) -> Guild:
        return self._data[idx]

    def seedOf(self, guild: Guild) -> int:
        return self._data.index(guild)

    def _load_data(self) -> List[Guild]:
        if self.season is None:
            return list(Guild.objects.order_by('name').all())
        elif self.season.completed():
            return self.season.playoffs[:] + self.season.standings[4:]
        return self.season.standings[:]

from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from ravnica.models import Season
    
from collections import OrderedDict
from django.apps import apps
from tabulate import tabulate

from ravnica.algorithms import generate_tiebreaker
from ravnica.enums import RecordType
from ravnica.models import Record, Guild


class Standings:
    def __init__(self, season: Season = None, guild: Guild = None, type: RecordType = RecordType.all()):
        self.season: Season = season
        self.guild: Guild = guild
        self.type: RecordType = type
        self._data: OrderedDict[Guild, Record] = self._load_data()

    def __str__(self) -> str:
        return tabulate([
            [guild.name, str(record), f'{record.win_pct:.2f}'] for guild, record in self._data.items()
        ], headers=['Guild', 'Record', 'Win%'])

    def __repr__(self) -> str:
        strs = []
        if self.season is not None:
            strs.append(f'season={self.season}')
        if self.guild is not None:
            strs.append(f'guild={self.guild}')
        return f'Standings({", ".join([x for x in strs])})'

    def __getitem__(self, idx: int) -> Guild:
        return list(self._data)[idx]

    def placeOf(self, guild: Guild) -> int:
        return list(self._data).index(guild)

    def __iter__(self):
        return iter(self._data.items())

    def _load_data(self) -> OrderedDict[Guild, Record]:
        guilds: List[Guild] = list(apps.get_model('ravnica', 'Guild').objects.order_by('name').all())

        records = {g: g.record(season=self.season, versus=self.guild, type=self.type) for g in guilds}
        for guild, record in records.items():
            record.tiebreaker = generate_tiebreaker(hero=guild, record_map=records, season=self.season)
            
        if self.guild is not None:
            records.pop(guild)
            records = {g: r.invert() for g, r in records.items()}

        return OrderedDict(sorted(records.items(), key=lambda x: x[1], reverse=True))
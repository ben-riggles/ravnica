from collections import OrderedDict
from django.apps import apps
from tabulate import tabulate
from typing import Dict

from core.algorithms import tiebreaker
from core.enums import RecordType
from core.models import Record


class Standings:
    def __init__(self, season:'Season' = None, guild:'Guild' = None, type:RecordType = RecordType.all()):
        self.season: 'Season' = season
        self.guild: 'Guild' = guild
        self.type: RecordType = type
        self._data: Dict['Guild', Record] = self._load_data()

    def __str__(self):
        return tabulate([
            [guild.name, str(record), f'{record.win_pct:.2f}'] for guild, record in self._lookup.items()
        ], headers=['Guild', 'Record', 'Win%'])

    def __repr__(self):
        strs = []
        if self.season is not None:
            strs.append(f'season={self.season}')
        if self.guild is not None:
            strs.append(f'guild={self.guild}')
        return f'Standings({", ".join([x for x in strs])})'

    def _load_data(self):
        guilds = list(apps.get_model('ravnica', 'Guild').objects.order_by('name').all())

        records = {}
        for guild in guilds:
            record = guild.record(season=self.season, versus=self.guild, type=self.type)

        records: Dict['Guild', Record] = {g: g.record(season=season, versus=guild) for g in guilds}
        records = {tiebreaker(guild=guild, record=record, record_map=records) for guild, record in records.items()}
        if self.guild is not None:
            records.pop(guild)
            records = {g: r.invert() for g, r in records.items()}

        self._lookup = OrderedDict(sorted(records.items(), key=lambda x: x[1], reverse=True))
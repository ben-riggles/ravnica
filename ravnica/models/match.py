from __future__ import annotations
from django.db import models
from typing import List

from core.algorithms import round_robin
from core.enums import RoundType


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey('ravnica.Season', on_delete=models.CASCADE)
    round = models.IntegerField(choices=RoundType.choices)
    away = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='away_set')
    home = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='home_set')
    winner = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='winner_set')

    def __str__(self):
        if self.away is None or self.home is None:
            return f'{self.round}: TBD @ TBD'
        return f'{self.round}: {str(self.away)} @ {str(self.home)}'

    def __repr__(self):
        if self.away is None or self.home is None:
            return f'Match(season={self.season}, round={self.round})'
        return f'Match(season={self.season}, round={self.round}, {self.away.guild.name} @ {self.home.guild.name})'
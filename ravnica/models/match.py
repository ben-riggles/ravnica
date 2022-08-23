from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ravnica.models import Deck, Season
    
from django.db import models
from ravnica.enums import RoundType


class Match(models.Model):
    id: int = models.AutoField(primary_key=True)
    season: Season = models.ForeignKey('ravnica.Season', on_delete=models.CASCADE)
    round: RoundType = models.IntegerField(choices=RoundType.choices)
    away: Deck = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='away_set')
    home: Deck = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='home_set')
    winner: Deck = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='winner_set')

    def __str__(self) -> str:
        if self.away is None or self.home is None:
            return f'{self.round}: TBD @ TBD'
        return f'{self.round}: {str(self.away)} @ {str(self.home)}'

    def __repr__(self) -> str:
        if self.away is None or self.home is None:
            return f'Match(season={self.season}, round={self.round})'
        return f'Match(season={self.season}, round={self.round}, {self.away.guild.name} @ {self.home.guild.name})'

    @property
    def loser(self) -> Deck | None:
        if self.winner:
            return self.home if self.away == self.winner else self.away
        return None

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

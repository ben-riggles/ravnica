from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ravnica.models import Guild, Season
    
from django.db import models
from ravnica.models import BaseModel, Record


class DeckLoadError(Exception):
    pass


class Deck(BaseModel):
    guild: Guild = models.ForeignKey('ravnica.Guild', on_delete=models.CASCADE)
    current: bool = models.BooleanField(default=False)
    content: bool = models.BinaryField()
    name: str = models.CharField(max_length=100, default='')

    def __str__(self) -> str:
        name = self.name if self.name else 'N/A'
        return f'{name} ({self.guild.name})'

    def __repr__(self) -> str:
        name = self.name if self.name else 'N/A'
        return f'Deck({self.guild.name} "{name}")'

    def record(self, season: Season = None, versus: Guild | Deck = None) -> Record:
        match_set = self.away_set.all() | self.home_set.all()
        if season is not None:
            match_set = match_set.filter(season=season)
        if versus is not None:
            if isinstance(versus, Guild):
                match_set = match_set.filter(models.Q(away__guild = versus) | models.Q(home__guild = versus))
            else:
                match_set = match_set.filter(models.Q(away = versus) | models.Q(home = versus))
            
        win_count = len(match_set.filter(winner=self))
        return Record(wins=win_count, losses=len(match_set) - win_count)
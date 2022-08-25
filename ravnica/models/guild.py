from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ravnica.models import Season

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pathlib import Path

from ravnica.utils import Paths
from ravnica.enums import RecordType, RoundType
from ravnica.models import BaseModel, Record, Deck, Match
from ravnica.models.deck import DeckLoadError


class Guild(BaseModel):
    name: str = models.CharField(max_length=10)
    full_name: str = models.CharField(max_length=50)
    short_name: str = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Guild({self.short_name})'

    @property
    def deck(self, season: Season = None) -> Deck:
        if season is None:
            return self.deck_set.get(current=True)
        example_match: Match = season.match_set.filter(models.Q(away__guild = self) | models.Q(home__guild = self)).first()
        return example_match.away if example_match.away.guild == self else example_match.home

    @property
    def deck_path(self) -> Path:
        return Paths.DECK_DIR.joinpath(f'{self.name.lower()}.cod')

    def record(self, season: Season = None, versus: Deck | Guild = None, type: RecordType = RecordType.all()) -> Record:
        match_set = Match.objects.filter(models.Q(away__guild = self) | models.Q(home__guild = self))
        if season is not None:
            match_set = match_set.filter(season=season)
        if versus is not None:
            if isinstance(versus, Deck):
                match_set = match_set.filter(models.Q(away = versus) | models.Q(home = versus))
            else:
                match_set = match_set.filter(models.Q(away__guild = versus) | models.Q(home__guild = versus))
        if type & RecordType.REGULAR_SEASON and not type & RecordType.PLAYOFFS:
            match_set = match_set.filter(round__lte=RoundType.R9)
        if type & RecordType.PLAYOFFS and not type & RecordType.REGULAR_SEASON:
            match_set = match_set.filter(round__gt=RoundType.R9)

        win_count = len(match_set.filter(winner__guild=self))
        return Record(wins=win_count, losses=len(match_set) - win_count)


@receiver(post_save, sender=Guild)
def deck_init(instance:Guild, raw:bool, **kwargs):
    if not raw:
        return

    if (instance.deck_path.exists()):
        with open(instance.deck_path, mode='rb') as blob:
            Deck(guild=instance, current=True, content=blob.read()).save()
    else:
        raise DeckLoadError(f'Could not find deck: {instance.deck_path}')
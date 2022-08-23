from __future__ import annotations
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pathlib import Path

from core import Paths
from core.enums import RecordType, RoundType
from core.models import Record
from ravnica.models import Deck, Match
from ravnica.models.deck import DeckLoadError


class Guild(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Guild({self.name})'

    @property
    def current_deck(self) -> Deck:
        return self.deck_set.get(current=True)

    @property
    def deck_path(self) -> Path:
        return Paths.DECK_DIR.joinpath(f'{self.name.lower()}.cod')

    def record(self, season:'Season' = None, versus:'Guild' = None, type=RecordType.all()):
        match_set = Match.objects.filter(models.Q(away__guild = self) | models.Q(home__guild = self))
        if season is not None:
            match_set = match_set.filter(season=season)
        if versus is not None:
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
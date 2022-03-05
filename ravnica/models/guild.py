from __future__ import annotations
from django.db import models
from django.db.models.signals import post_save
from pathlib import Path

from core import Paths
from ravnica.models import Deck


class Guild(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=50)

    @property
    def current_deck(self) -> Deck:
        return self.deck_set.get(current=True)

    @property
    def deck_path(self) -> Path:
        return Paths.DECK_DIR.joinpath(f'{self.name.lower()}.cod')

    @staticmethod
    def handler(instance:Guild, **kwargs):
        if (instance.deck_path.exists()):
            deck = Deck(guild=instance.id, current=True, content='')


post_save.connect(Guild.handler, sender=Guild)
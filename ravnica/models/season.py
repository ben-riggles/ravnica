from __future__ import annotations
from django.db import models

from core.enums import RoundType
from ravnica.models import Round


class Season(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    name = models.CharField(max_length=200)
    current = models.BooleanField(default=False)

    @staticmethod
    def new(number, name='') -> Season:
        season = Season(number=number, name=name)
        for rd in RoundType:
            round = Round.new(rd)
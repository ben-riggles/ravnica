from __future__ import annotations
from django.db import models

from core.enums import RoundType
from core.models import Seedings
from ravnica.models import Round


class Season(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    name = models.CharField(max_length=200)
    current = models.BooleanField(default=False)
    previous = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.SET_NULL)

    @staticmethod
    def new(name:str ='', prev:Season = None) -> Season:
        number = 0 if prev is None else prev.id + 1
        season = Season(number=number, name=name, previous=prev.id)

        for rd in RoundType:
            round = Round.new(rd)
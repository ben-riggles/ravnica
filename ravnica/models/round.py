from __future__ import annotations
from django.db import models

from core.algorithms import round_robin
from core.enums import RoundType
from core.models import Seedings
from ravnica.models import Match


class Round(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey('ravnica.Season', on_delete=models.CASCADE)
    playoff = models.BooleanField(default=False)
    type = models.IntegerField(choices=RoundType.choices)

    @staticmethod
    def new(rd: RoundType, season: int) -> Round:
        round = Round(season=season, type=rd)
        round.playoff = rd > RoundType.R9

        for matchup in round_robin(rd):
            match = Match(round=round.id, away=matchup)
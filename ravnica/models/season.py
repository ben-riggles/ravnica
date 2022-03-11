from __future__ import annotations
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.algorithms import round_robin
from core.enums import RoundType
from core.models import Seeding, Standings
from ravnica.models import Match


class PostseasonError(Exception):
    pass


class Season(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    name = models.CharField(max_length=200, default='')
    previous = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def seeding(self) -> Seeding:
        return Seeding(season=self)

    @property
    def standings(self) -> Standings:
        return Standings()

    def __str__(self):
        if self.name:
            return f'Season {self.number}: {self.name}'
        return f'Season {self.number}'

    def __repr__(self):
        return f'Season({self.number})'

    @staticmethod
    def new(name:str = '', prev:Season = None) -> Season:
        number = 0 if prev is None else prev.number + 1
        season = Season(number=number, name=name, previous=prev)
        seeding = Seeding(season=prev)
        season.save()

        for rd in RoundType:
            for matchup in round_robin(rd):
                try:
                    away = seeding[matchup[0]].current_deck
                    home = seeding[matchup[1]].current_deck
                except TypeError:
                    away = home = None
                m = Match(season=season, round=rd, away=away, home=home)

                import random
                m.winner = away if random.randint(0, 1) == 0 else home
                m.save()
        return season


@receiver(post_save, sender=Match)
def update_postseason(instance:Match, **kwargs):
    return
    season = instance.season

    # Check if all regular season matches are complete
    if season.match_set.filter(round__lte=RoundType.R9, winner__isnull=True):
        return

    # Check if finals are complete
    if season.match_set.filter(round=RoundType.FINALS, winner__isnull=False):
        return

    # Check if semifinals are complete
    if season.match_set.filter(round__gt=RoundType.SEMIFINALS, winner__isnull=False):
        winners = [match.winner for match in season.match_set.filter(round=RoundType.FINALS)]
        if len(winners) != 2:
            raise PostseasonError('There should be exactly 2 winners from the semifinal round')
        winners = sorted(winners, key=lambda x: x.record)
        season.match_set.get(round=RoundType.FINALS).update(
            away=winners[0], home=winners[1]
        )
        return

    # Create the playoff matchups
    playoff_teams = season.standings[0:3]
    sf_matches = season.match_set.filter(round=RoundType.SEMIFINALS)
    if len(sf_matches) != 2:
        raise PostseasonError('There should be exactly 2 semifinal matches in a season')
    sf_matches[0].update(home=playoff_teams[0].current_deck, away=playoff_teams[3].current_deck)
    sf_matches[1].update(home=playoff_teams[1].current_deck, away=playoff_teams[2].current_deck)
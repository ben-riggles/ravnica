from __future__ import annotations
from turtle import update
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.algorithms import round_robin
from core.enums import RoundType, RecordType
from core.models import Playoffs, Seeding, Standings
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
        return Seeding(season=self.previous)

    @property
    def new_seeding(self) -> Seeding:
        return Seeding(season=self)

    @property
    def playoffs(self):
        return Playoffs(season=self)

    @property
    def standings(self) -> Standings:
        return Standings(season=self, type=RecordType.REGULAR_SEASON)

    def __str__(self):
        if self.name:
            return f'Season {self.number}: {self.name}'
        return f'Season {self.number}'

    def __repr__(self):
        return f'Season({self.number})'

    @property
    def winner(self):
        return self.match_set.filter(round=RoundType.FINALS).winner

    @property
    def current_round(self) -> RoundType:
        try:
            round = self.match_set.filter(winner__isnull=False).order_by('-round')[0].round
        except IndexError:
            return RoundType.R1

        if self.match_set.filter(round=round, winner__isnull=True):
            return RoundType(round)
        return RoundType(round+1)

    def regular_season_completed(self) -> bool:
        return self.current_round > RoundType.R9

    def completed(self) -> bool:
        return self.current_round == RoundType.COMPLETED

    @staticmethod
    def new(name:str = '', prev:Season = None) -> Season:
        number = 1 if prev is None else prev.number + 1
        season = Season(number=number, name=name, previous=prev)
        season.save()

        seeding = season.seeding
        for rd in RoundType:
            for matchup in round_robin(rd):
                try:
                    away = seeding[matchup[0]].current_deck
                    home = seeding[matchup[1]].current_deck
                except TypeError:
                    away = home = None
                Match(season=season, round=rd, away=away, home=home).save()

        import random
        for m in season.match_set.filter(round__lte=RoundType.R9):
            m.update(winner=m.away if random.randint(0, 1) == 0 else m.home)
        return season


@receiver(post_save, sender=Match)
def update_postseason(instance:Match, **kwargs):
    season = instance.season

    # Check if any regular season matches are incomplete or if the season is complete
    if not season.regular_season_completed() or season.completed():
        return

    # Check if semifinals are complete
    if season.current_round == RoundType.FINALS:
        winners = [match.winner for match in season.match_set.filter(round=RoundType.SEMIFINALS)]
        if len(winners) != 2:
            raise PostseasonError('There should be exactly 2 winners from the semifinal round')
        winners = sorted(winners, key=lambda x: x.record(season=season))

        # TEMPORARY COIN FLIP
        import random
        season.match_set.get(round=RoundType.FINALS).update(away=winners[0], home=winners[1],
        winner=winners[random.randint(0,1)])
        return

    # Check if postseason has already been created
    if season.match_set.filter(round=RoundType.SEMIFINALS, home__isnull=False):
        return

    # Create the playoff matchups
    playoff_teams = season.standings[0:4]
    sf_matches = season.match_set.filter(round=RoundType.SEMIFINALS)
    if len(sf_matches) != 2:
        raise PostseasonError('There should be exactly 2 semifinal matches in a season')
    sf_matches[0].update(home=playoff_teams[0].current_deck, away=playoff_teams[3].current_deck)
    sf_matches[1].update(home=playoff_teams[1].current_deck, away=playoff_teams[2].current_deck)

    # TEMPORARY COIN FLIP
    import random
    for m in sf_matches:
        m.update(winner=m.away if random.randint(0, 1) == 0 else m.home)
from __future__ import annotations
from typing import TYPE_CHECKING, List
from ravnica.enums.round_type import RoundType
from ravnica.models.guild import Guild
if TYPE_CHECKING:
    from ravnica.models import Season

from ravnica.models import Match


class Playoffs:
    def __init__(self, season: Season):
        self.season = season
        
    def __str__(self) -> str:
         return self.ranking()

    def __repr__(self) -> str:
        return f'Playoffs(season={self.season.id})'

    def __getitem__(self, idx: int) -> Guild:
        return self.ranking()[idx]

    def semifinals(self) -> List[Match]:
        return list(self.season.match_set.filter(round=RoundType.SEMIFINALS))

    def finals(self) -> Match:
        return self.season.match_set.get(round=RoundType.FINALS)

    def initial_seeding(self) -> List[Guild]:
        return self.season.standings[:4]

    def ranking(self) -> List[Guild]:
        if self.season.completed():
            seeding = self.initial_seeding()
            semi_losers = sorted([x.loser for x in self.semifinals()], key=lambda x: seeding.index(x.guild))
            finals = self.finals()

            return [
                finals.winner.guild,
                finals.loser.guild,
                semi_losers[0].guild,
                semi_losers[1].guild,
            ]

            winners = [x.winner for x in semis]
            losers = [x.loser for x in semis]
        elif self.season.current_round == RoundType.FINALS:
            seeding = self.initial_seeding()
            semis = self.semifinals()
            winners = sorted([x.winner for x in semis], key=lambda x: seeding.index(x.guild))
            losers = sorted([x.loser for x in semis], key=lambda x: seeding.index(x.guild))

            return [
                winners[0].guild,
                winners[1].guild,
                losers[0].guild,
                losers[1].guild
            ]
        elif self.season.current_round == RoundType.SEMIFINALS:
            return self.initial_seeding()
        return []
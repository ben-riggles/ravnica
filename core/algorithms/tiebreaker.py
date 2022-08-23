from __future__ import annotations
from __future__ import annotations
from collections import OrderedDict
from django.db import models

from core.enums import TiebreakerMethod, RoundType, RecordType


class Tiebreaker:
    def __init__(self):
        self._data: OrderedDict = OrderedDict([(x, 0) for x in TiebreakerMethod])

    def __getitem__(self, idx: TiebreakerMethod) -> int | None:
        return self._data[idx]

    def __setitem__(self, idx: TiebreakerMethod, val: int):
        self._data[idx] = val

    def __lt__(self, other: Tiebreaker) -> bool:
        for method in TiebreakerMethod:
            if self[method] == other[method]:
                continue
            return self[method] < other[method]
        return False

    def __gt__(self, other: Tiebreaker) -> bool:
        for method in TiebreakerMethod:
            if self[method] == other[method]:
                continue
            return self[method] > other[method]
        return False


def head_to_head(hero, record_map, season) -> int:
    hero_rec = record_map[hero]
    ties = [k for k, v in record_map.items() if v == hero_rec and k != hero]
    h2h = [hero.record(season=season, versus=x) for x in ties]

    h2h_record = None
    for x in h2h:
        h2h_record = h2h_record + x if h2h_record else x
    return h2h_record.win_pct if h2h_record else 0


def strength_of_schedule(hero, season) -> int:
    match_set = season.match_set.filter(round__lte=RoundType.R9, winner__guild=hero)
    villains = [x.away.guild if x.away.guild != hero else x.home.guild for x in match_set]
    return sum([v.record(season=season, type=RecordType.REGULAR_SEASON).wins for v in villains])


def seeding(hero, seeding) -> int:
    return 10 - seeding.seedOf(hero)


def generate_tiebreaker(hero, record_map=None, season=None) -> Tiebreaker:
    tb = Tiebreaker()
    if season:
        if record_map:
            tb[TiebreakerMethod.HEAD_TO_HEAD] = head_to_head(hero, record_map, season)
        tb[TiebreakerMethod.STR_OF_SCHED] = strength_of_schedule(hero, season)
        tb[TiebreakerMethod.SEEDING] = seeding(hero, season.seeding)
    return tb

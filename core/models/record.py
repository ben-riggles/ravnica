from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from core.enums import TiebreakerMethod


@dataclass
class Record:
    wins: int
    losses: int
    tiebreaker: Dict[TiebreakerMethod, int] = {}

    def __str__(self):
        return f'{self.wins}-{self.losses}'

    def __repr__(self):
        return f'Record ({str(self)})'

    def __lt__(self, other:Record):
        if self.win_pct != other.win_pct:
            return self.win_pct < other.win_pct

        # Get all tiebreaker values that are shared and unequal
        tiebreaker = {k: v for k, v in self.tiebreaker.items() if k in other.tiebreaker and other.tiebreaker[k] != v}
        if TiebreakerMethod.HEAD_TO_HEAD in tiebreaker:
            return self.tiebreaker[TiebreakerMethod.HEAD_TO_HEAD] < other.tiebreaker[TiebreakerMethod.HEAD_TO_HEAD]
        elif TiebreakerMethod.STR_OF_SCHED in tiebreaker:
            return self.tiebreaker[TiebreakerMethod.STR_OF_SCHED] < other.tiebreaker[TiebreakerMethod.STR_OF_SCHED]
        elif TiebreakerMethod.SEEDING in tiebreaker:
            return self.tiebreaker[TiebreakerMethod.SEEDING] < other.tiebreaker[TiebreakerMethod.SEEDING]
        return False

    def __gt__(self, other:Record):
        if self.win_pct != other.win_pct:
            return self.win_pct > other.win_pct

        # Get all tiebreaker values that are shared and unequal
        tiebreaker = {k: v for k, v in self.tiebreaker.items() if k in other.tiebreaker and other.tiebreaker[k] != v}
        if TiebreakerMethod.HEAD_TO_HEAD in tiebreaker:
            return self.tiebreaker[TiebreakerMethod.HEAD_TO_HEAD] > other.tiebreaker[TiebreakerMethod.HEAD_TO_HEAD]
        elif TiebreakerMethod.STR_OF_SCHED in tiebreaker:
            return self.tiebreaker[TiebreakerMethod.STR_OF_SCHED] > other.tiebreaker[TiebreakerMethod.STR_OF_SCHED]
        elif TiebreakerMethod.SEEDING in tiebreaker:
            return self.tiebreaker[TiebreakerMethod.SEEDING] > other.tiebreaker[TiebreakerMethod.SEEDING]
        return False

    def __eq__(self, other:Record):
        return self.win_pct == other.win_pct

    @property
    def win_pct(self) -> float:
        return self.wins / (self.wins + self.losses)

    def invert(self) -> Record:
        return Record(wins=self.losses, losses=self.wins)
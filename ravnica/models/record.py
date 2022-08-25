from __future__ import annotations

from dataclasses import dataclass

from ravnica.algorithms.tiebreaker import Tiebreaker


@dataclass
class Record:
    wins: int = 0
    losses: int = 0
    tiebreaker: Tiebreaker = Tiebreaker()

    def __str__(self) -> str:
        return f'{self.wins}-{self.losses}'

    def __repr__(self) -> str:
        return f'Record ({str(self)})'

    def __add__(self, other: Record) -> Record:
        return Record(
            wins=self.wins + other.wins,
            losses=self.losses + other.losses
        )

    def __lt__(self, other:Record) -> bool:
        if self.win_pct != other.win_pct:
            return self.win_pct < other.win_pct
        return self.tiebreaker < other.tiebreaker

    def __gt__(self, other:Record) -> bool:
        if self.win_pct != other.win_pct:
            return self.win_pct > other.win_pct
        return self.tiebreaker > other.tiebreaker

    def __eq__(self, other:Record) -> bool:
        return self.win_pct == other.win_pct and self.tiebreaker == other.tiebreaker

    def __len__(self) -> int:
        return self.wins + self.losses

    @property
    def win_pct(self) -> float:
        try:
            return float(self.wins / len(self))
        except ZeroDivisionError:
            return 0.0

    def invert(self) -> Record:
        return Record(wins=self.losses, losses=self.wins)
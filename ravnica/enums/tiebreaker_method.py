from enum import Enum, auto


class TiebreakerMethod(Enum):
    HEAD_TO_HEAD = auto()
    STR_OF_SCHED = auto()
    SEEDING = auto()
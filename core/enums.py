from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum, Flag, auto


class RoundType(models.IntegerChoices):
    R1 = 1, _('Round One')
    R2 = 2, _('Round Two')
    R3 = 3, _('Round Three')
    R4 = 4, _('Round Four')
    R5 = 5, _('Round Five')
    R6 = 6, _('Round Six')
    R7 = 7, _('Round Seven')
    R8 = 8, _('Round Eight')
    R9 = 9, _('Round Nine')
    SEMIFINALS = 10, _('Semifinals')
    FINALS = 11, _('Finals')
    COMPLETED = 12, _('Completed')


class RecordType(Flag):
    REGULAR_SEASON = auto()
    PLAYOFFS = auto()

    @classmethod
    def all(_):
        return RecordType.REGULAR_SEASON & RecordType.PLAYOFFS


class TiebreakerMethod(Enum):
    HEAD_TO_HEAD = auto()
    STR_OF_SCHED = auto()
    SEEDING = auto()
from enum import Flag, auto


class RecordType(Flag):
    REGULAR_SEASON = auto()
    PLAYOFFS = auto()

    @classmethod
    def all(_):
        return RecordType.REGULAR_SEASON & RecordType.PLAYOFFS
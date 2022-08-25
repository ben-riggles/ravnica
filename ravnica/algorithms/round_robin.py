from typing import List, Tuple

from ravnica.enums import RoundType


def round_robin(round: RoundType) -> List[Tuple[int]]:
    match round:
        case RoundType.R1:
            return [(9, 0), (8, 1), (7, 2), (6, 3), (5, 4)]
        case RoundType.R2:
            return [(0, 8), (1, 7), (2, 6), (3, 5), (4, 9)]
        case RoundType.R3:
            return [(7, 0), (6, 1), (5, 2), (9, 3), (8, 4)]
        case RoundType.R4:
            return [(0, 3), (1, 4), (2, 9), (5, 7), (6, 8)]
        case RoundType.R5:
            return [(0, 6), (1, 5), (4, 2), (3, 8), (7, 9)]
        case RoundType.R6:
            return [(4, 0), (2, 1), (3, 7), (8, 5), (9, 6)]
        case RoundType.R7:
            return [(5, 0), (9, 1), (8, 2), (4, 3), (7, 6)]
        case RoundType.R8:
            return [(0, 2), (3, 1), (7, 4), (6, 5), (9, 8)]
        case RoundType.R9:
            return [(1, 0), (2, 3), (6, 4), (5, 9), (8, 7)]
        case RoundType.SEMIFINALS:
            return [(None, None), (None, None)]
        case RoundType.FINALS:
            return [(None, None)]
        case _:
            return []
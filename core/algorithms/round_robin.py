from typing import List, Tuple

from core.enums import RoundType


def round_robin(round: RoundType) -> List[Tuple[int]]:
    match round:
        case RoundType.R1:
            return [(10, 1), (9, 2), (8, 3), (7, 4), (6, 5)]
        case RoundType.R2:
            return [(1, 9), (2, 8), (3, 7), (4, 6), (5, 10)]
        case RoundType.R3:
            return [(8, 1), (7, 2), (6, 3), (10, 4), (9, 5)]
        case RoundType.R4:
            return [(1, 4), (2, 5), (3, 10), (6, 8), (7, 9)]
        case RoundType.R5:
            return [(1, 7), (2, 6), (5, 3), (4, 9), (8, 10)]
        case RoundType.R6:
            return [(5, 1), (3, 2), (4, 8), (9, 6), (10, 7)]
        case RoundType.R7:
            return [(6, 1), (10, 2), (9, 3), (5, 4), (8, 7)]
        case RoundType.R8:
            return [(1, 3), (4, 2), (8, 5), (7, 6), (10, 9)]
        case RoundType.R9:
            return [(2, 1), (3, 4), (7, 5), (6, 10), (9, 8)]
        case RoundType.SEMIFINALS:
            return [(None, None), (None, None)]
        case RoundType.FINALS:
            return [(None, None)]
        case _:
            return []
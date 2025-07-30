from enum import Enum, auto


class Status(Enum):
    GAME_START = auto()
    IN_PLAY = auto()
    WIN = auto()
    LOSS = auto()

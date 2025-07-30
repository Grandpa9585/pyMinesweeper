from dataclasses import dataclass


@dataclass
class Cell:
    is_bomb: bool
    is_hidden: bool
    is_flagged: bool
    is_wrong_flag: bool
    num_bombs: int


@dataclass
class Cursor:
    x: int
    y: int

from typing import Protocol

from .model_constants import Status
from .model_types import Cell, Cursor


class ModelInterface(Protocol):
    def generate_bombs(self) -> None:
        ...

    def reveal_cell(self) -> None:
        ...

    def flag_cell(self) -> None:
        ...

    def move_cursor(self, di: int, dj: int) -> None:
        ...

    def get_cell(self, i: int, j: int) -> Cell:
        ...

    def auto_clear(self) -> None:
        ...

    @property
    def status(self) -> Status:
        ...

    @status.setter
    def status(self, v: Status) -> None:
        ...

    @property
    def width(self) -> int:
        ...

    @property
    def height(self) -> int:
        ...

    @property
    def flags(self) -> int:
        ...

    @property
    def cursor(self) -> Cursor:
        ...

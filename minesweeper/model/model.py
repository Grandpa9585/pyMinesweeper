from random import randint
from typing import List

from .model_constants import Status
from .model_types import Cell, Cursor


class Model:
    def __init__(self, width: int, height: int, num_bombs: int) -> None:
        self._status: Status = Status.GAME_START
        self._width: int = width
        self._height: int = height
        self._num_bombs: int = num_bombs
        self._flags: int = num_bombs
        self._revealed_cells: int = 0
        self._grid: List[List[Cell]] = [
            [Cell(False, True, False, False, 0) for _ in range(width)]
            for _ in range(height)
        ]
        self._cursor: Cursor = Cursor(0, 0)

    def generate_bombs(self) -> None:
        for _ in range(self._num_bombs):
            while True:
                i: int = randint(0, self._height - 1)
                j: int = randint(0, self._width - 1)
                cell: Cell = self._grid[i][j]

                if cell.is_bomb:
                    continue

                if (i, j) in {
                    (self._cursor.x + di, self._cursor.y + dj)
                        for di in range(-2, 3) for dj in range(-2, 3)}:
                    continue

                cell.is_bomb = True
                cell.num_bombs = -1
                self._increment_neighbors(i, j)
                break

    def _increment_neighbors(self, i: int, j: int) -> None:
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) == (0, 0):
                    continue

                if 0 <= i + di < self.height and 0 <= j + dj < self.width:
                    cell: Cell = self._grid[i + di][j + dj]
                else:
                    continue

                if cell.is_bomb:
                    continue

                cell.num_bombs += 1

    def _reveal_all(self) -> None:
        for row in self._grid:
            for cell in row:
                cell.is_hidden = False
                if cell.is_flagged and not cell.is_bomb:
                    cell.is_wrong_flag = True
        self._cursor = Cursor(-1, -1)

    def reveal_cell(self) -> None:
        cell: Cell = self._grid[self._cursor.x][self._cursor.y]
        if cell.is_bomb:
            if cell.is_flagged:
                return None
            self._status = Status.LOSS
            self._reveal_all()
        else:
            self._auto_reveal(self._cursor.x, self._cursor.y)
            if self._revealed_cells + self._num_bombs == self._width * self._height:
                self._status = Status.WIN
                self._reveal_all()

    def auto_clear(self) -> None:
        cell: Cell = self._grid[self._cursor.x][self._cursor.y]
        if cell.is_hidden:
            return None
        if cell.num_bombs == self._count_flagged(self._cursor.x, self._cursor.y):
            self._clear_surrounding(self._cursor.x, self._cursor.y)

    def _clear_surrounding(self, i: int, j: int) -> None:
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) == (0, 0):
                    continue
                if 0 <= i + di < self.height and 0 <= j + dj < self.width:
                    self._cursor = Cursor(i + di, j + dj)
                else:
                    continue
                self.reveal_cell()
        self._cursor = Cursor(i, j)

    def _count_flagged(self, i: int, j: int) -> int:
        ret = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) == (0, 0):
                    continue
                if 0 <= i + di < self.height and 0 <= j + dj < self.width:
                    ret += 1 if self._grid[i + di][j + dj].is_flagged else 0
                else:
                    continue
        return ret

    def _auto_reveal(self, i: int, j: int) -> None:
        if not (0 <= i < self._height and 0 <= j < self._width):
            return None

        cell: Cell = self._grid[i][j]

        if cell.is_flagged:
            return None

        if not cell.is_hidden:
            return None
        elif cell.num_bombs > 0:
            cell.is_hidden = False
            self._revealed_cells += 1
            return None

        cell.is_hidden = False
        self._revealed_cells += 1

        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) == (0, 0):
                    continue
                self._auto_reveal(i + di, j + dj)

    def flag_cell(self) -> None:
        cell: Cell = self._grid[self._cursor.x][self._cursor.y]
        if not cell.is_hidden:
            return None

        if cell.is_flagged:
            cell.is_flagged = False
            self._flags -= 1
        else:
            cell.is_flagged = True
            self._flags += 1

    def move_cursor(self, di: int, dj: int) -> None:
        if 0 <= self._cursor.x + di < self._height and 0 <= self._cursor.y + dj < self._width:
            self._cursor.x += di
            self._cursor.y += dj

    def get_cell(self, i: int, j: int) -> Cell:
        return self._grid[i][j]

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, v: Status) -> None:
        self._status = v

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def flags(self) -> int:
        return self._flags

    @property
    def cursor(self) -> Cursor:
        return self._cursor

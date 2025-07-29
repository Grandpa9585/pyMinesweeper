from getkey import getkey, keys  # type: ignore
# import numpy as np

from enum import Enum, auto
from typing import List, Tuple, Dict
from dataclasses import dataclass
from random import randint
from os import system


class Status(Enum):
    IN_PLAY = auto()
    LOSS = auto()
    WIN = auto()


@dataclass
class Cell:
    is_selected: bool
    is_bomb: bool
    is_hidden: bool
    is_flagged: bool
    num_surround_bombs: int


class Model():
    def __init__(self, width: int, height: int, num_bombs: int) -> None:
        self.width: int = width
        self.height: int = height
        self.num_bombs: int = num_bombs
        self.cells_revealed: int = 0
        self.grid: List[List[Cell]] = [
            [Cell(False, False, True, False, 0) for _ in range(width)] for _ in range(height)]
        self.status: Status = Status.IN_PLAY
        self.selected_cell: Tuple[int, int] = (0, 0)
        self.grid[self.selected_cell[0]
                  ][self.selected_cell[1]].is_selected = True

        self._init_generate_bombs()

    def _init_generate_bombs(self) -> None:
        for _ in range(self.num_bombs):
            while True:
                i: int = randint(0, self.height - 1)
                j: int = randint(0, self.width - 1)
                if not self.grid[i][j].is_bomb:
                    self.grid[i][j].is_bomb = True
                    self.grid[i][j].num_surround_bombs = -1
                    self._init_increment_neighbors(i, j)
                    break

    def _init_increment_neighbors(self, x: int, y: int) -> None:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if 0 <= x + i < self.height and 0 <= y + j < self.width:
                    if self.grid[x + i][y + j].is_bomb:
                        continue
                    self.grid[x + i][y + j].num_surround_bombs += 1
                else:
                    continue

    # def _convert_cartesian_to_two_array(self, x: int, y: int) -> Tuple[int, int]:
    #     return (self.height - y, x - 1)  # just dont think about it

    def reveal_cell(self, i: int, j: int) -> None:
        if self.grid[i][j].is_bomb:
            self.status = Status.LOSS
            self._reveal_all()
        else:
            self._auto_reveal(i, j)
            if self.cells_revealed + self.num_bombs == self.width * self.height:
                self.status = Status.WIN
                self._reveal_all()

    def flag_cell(self, i: int, j: int) -> None:
        if self.grid[i][j].is_hidden:
            self.grid[i][j].is_flagged = True
        else:
            self.grid[i][j].is_flagged = False

    def _auto_reveal(self, i: int, j: int) -> None:
        if not (0 <= i < self.height and 0 <= j < self.width):
            return None

        # if self.grid[i][j].num_surround_bombs > 0:
            # self.grid[i][j].is_hidden = False
            # return None

        if not self.grid[i][j].is_hidden:
            return None
        elif self.grid[i][j].num_surround_bombs > 0:
            self.grid[i][j].is_hidden = False
            self.cells_revealed += 1
            return None

        if self.grid[i][j].is_flagged:
            return None

        self.grid[i][j].is_hidden = False
        self.cells_revealed += 1

        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if (di, dj) == (0, 0):
                    continue
                self._auto_reveal(i + di, j + dj)

    def _reveal_all(self):
        for row in self.grid:
            for cell in row:
                cell.is_hidden = False


class View():
    number_to_emoji: Dict[int, str] = {
        1: '🕐',
        2: '🕑',
        3: '🕒',
        4: '🕓',
        5: '🕔',
        6: '🕕',
        7: '🕖',
        8: '🕗',
        9: '🕘',
    }

    def view(self, model: Model):
        print('|', *['_' for _ in range(model.width)], '|', sep='')
        for i in range(model.height):
            print('|', end='')
            for j in range(model.width):
                cell = model.grid[i][j]
                if (i, j) == model.selected_cell:
                    print('🟦', end='')
                elif cell.is_flagged:
                    print('🚩', end='')
                elif cell.is_hidden:
                    print('🧱', end='')
                elif cell.is_bomb:
                    print('💣', end='')
                elif cell.num_surround_bombs != 0:
                    print(
                        self.number_to_emoji[cell.num_surround_bombs], end='')
                    # print(cell.num_surround_bombs, ' ', end='')
                else:
                    print('🟩', end='')
            print('|')
        print('|', *['_' for _ in range(model.width)], '|', sep='')

    def clear_screen(self):
        system("clear")


class Control:
    def __init__(self, model: Model, view: View) -> None:
        self.model: Model = model
        self.view: View = view

    def run(self):
        self.view.clear_screen()
        self.view.view(self.model)
        while self.model.status == Status.IN_PLAY:
            key = getkey()  # type: ignore
            if key == keys.ENTER:  # type: ignore
                self.model.reveal_cell(
                    self.model.selected_cell[0], self.model.selected_cell[1])
            if key == 'f':
                self.model.flag_cell(
                    self.model.selected_cell[0], self.model.selected_cell[1])
            if key == 'w':
                self.model.selected_cell = (
                    self.model.selected_cell[0] - 1, self.model.selected_cell[1])
            if key == 'a':
                self.model.selected_cell = (
                    self.model.selected_cell[0], self.model.selected_cell[1] - 1)
            if key == 's':
                self.model.selected_cell = (
                    self.model.selected_cell[0] + 1, self.model.selected_cell[1])
            if key == 'd':
                self.model.selected_cell = (
                    self.model.selected_cell[0], self.model.selected_cell[1] + 1)
            self.view.clear_screen()
            self.view.view(self.model)


model = Model(20, 30, 70)
view = View()
control = Control(model, view)

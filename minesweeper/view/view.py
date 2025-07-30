from os import system

from ..model.model_interface import ModelInterface
from ..model.model_types import Cell


class View:
    def clear_screen(self):
        system('clear')

    def view_grid(self, model: ModelInterface):
        for i in range(model.height):
            for j in range(model.width):
                if (i, j) == (model.cursor.x, model.cursor.y):
                    print('▒', end='')
                    continue

                cell: Cell = model.get_cell(i, j)

                if cell.is_flagged:
                    if cell.is_wrong_flag:
                        print('X', end='')
                    else:
                        print('░', end='')
                elif cell.is_hidden:
                    print('█', end='')
                elif cell.num_bombs > 0:
                    print(cell.num_bombs, end='')
                elif cell.num_bombs == 0:
                    print(' ', end='')
                elif cell.is_bomb:
                    print('▓', end='')
                else:
                    raise RuntimeError("Not exhaustive")
            print()

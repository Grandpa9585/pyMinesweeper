from os import system
from rich.console import Console
from rich.text import Text

from ..model.model_interface import ModelInterface
from ..model.model_types import Cell


class View:
    def __init__(self) -> None:
        self.console: Console = Console()

    def clear_screen(self):
        system('clear')

    def view_grid(self, model: ModelInterface):
        for i in range(model.height):
            for j in range(model.width):
                if (i, j) == (model.cursor.x, model.cursor.y):
                    # self._color_print('▒', 'bright_cyan', end='')
                    self._color_print('█', 'bright_cyan', end='')
                    continue

                cell: Cell = model.get_cell(i, j)

                if cell.is_flagged:
                    if cell.is_wrong_flag:
                        self._color_print('X', 'bright_red', end='')
                    else:
                        # self._color_print('░', 'red', end='')
                        self._color_print('█', 'bright_green', end='')
                elif cell.is_hidden:
                    print('█', end='')
                elif cell.num_bombs > 0:
                    print(cell.num_bombs, end='')
                elif cell.num_bombs == 0:
                    print(' ', end='')
                elif cell.is_bomb:
                    self._color_print('▓', 'red', end='')
                else:
                    raise RuntimeError("Not exhaustive")
            print()

    def _color_print(self, text: str, color: str, end: str = '\n') -> None:
        _text: Text = Text(text)
        _text.stylize(color)
        self.console.print(_text, end=end)

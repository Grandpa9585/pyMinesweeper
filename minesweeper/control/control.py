from getkey import getkey, keys  # type: ignore

from ..model.model_interface import ModelInterface
from ..model.model_constants import Status
from ..view.view_interface import ViewInterface


class Control:
    def __init__(self, model: ModelInterface, view: ViewInterface) -> None:
        self._model: ModelInterface = model
        self._view: ViewInterface = view

    def run(self) -> None:
        self._view.clear_screen()
        self._view.view_grid(self._model)

        while self._model.status == Status.IN_PLAY or self._model.status == Status.GAME_START:
            key: str = getkey()  # type: ignore
            if key == 'w':
                self._model.move_cursor(-1, 0)
            if key == 'a':
                self._model.move_cursor(0, -1)
            if key == 's':
                self._model.move_cursor(1, 0)
            if key == 'd':
                self._model.move_cursor(0, 1)
            if key == 'f':
                self._model.flag_cell()
            if key == keys.ENTER:  # type: ignore
                if self._model.status == Status.GAME_START:
                    self._model.status = Status.IN_PLAY
                    self._model.generate_bombs()

                self._model.reveal_cell()
                self._model.auto_clear()

            self._view.clear_screen()
            self._view.view_grid(self._model)

from typing import Protocol

from ..model.model_interface import ModelInterface


class ViewInterface(Protocol):
    def clear_screen(self):
        ...

    def view_grid(self, model: ModelInterface):
        ...

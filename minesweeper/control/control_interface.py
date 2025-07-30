from typing import Protocol


class ControlInterface(Protocol):
    def run(self) -> None:
        ...

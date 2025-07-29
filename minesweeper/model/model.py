from .model_constants import Status


class Model:
    def __init__(self) -> None:
        self.status: Status = Status.IN_PLAY

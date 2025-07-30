import sys

from .control.control import Control
from .control.control_interface import ControlInterface
from .model.model import Model
from .model.model_interface import ModelInterface
from .view.view import View
from .view.view_interface import ViewInterface


def main() -> None:
    if len(sys.argv) == 1:
        print('missing arguements for width height num_bombs')
        return None
    elif len(sys.argv) == 2:
        print('missing arguements for width height num_bombs')
        return None
    elif len(sys.argv) == 3:
        print('missing arguements for height num_bombs')
        return None
    elif len(sys.argv) >= 5:
        print('too many arguements')
        return None

    try:
        width: int = int(sys.argv[1])
        height: int = int(sys.argv[2])
        num_bombs: int = int(sys.argv[3])
    except ValueError:
        print("at least one value is a non-integer")
        return None

    model: ModelInterface = Model(width, height, num_bombs)
    view: ViewInterface = View()
    control: ControlInterface = Control(model, view)

    control.run()


main()

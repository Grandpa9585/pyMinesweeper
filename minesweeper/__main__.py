from .control.control import Control
from .control.control_interface import ControlInterface
from .model.model import Model
from .model.model_interface import ModelInterface
from .view.view import View
from .view.view_interface import ViewInterface

model: ModelInterface = Model(20, 30, 100)
view: ViewInterface = View()
control: ControlInterface = Control(model, view)

control.run()

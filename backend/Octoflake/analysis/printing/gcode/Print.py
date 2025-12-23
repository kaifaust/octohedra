import math
from dataclasses import dataclass, field
from typing import List

from printing.gcode.Move import Move, MoveConfig
from printing.gcode.PrinterConfig import PrinterConfig
from printing.gcode.TempConfig import TempConfig











@dataclass
class LayerConfig:
    temp_config: TempConfig = TempConfig()
    default_move_config: MoveConfig = MoveConfig()



@dataclass
class Layer:
    """Represents all the moves that will be made in a flat horizontal layer"""
    layer_config : LayerConfig
    index: int = None
    z_bottom: float = 0

    paths : List[Path] = field(default_factory=list)


    def new_path(self):
        path = Path()
        self.paths.append(path)
        return path



@dataclass
class Print:
    """Represents a full print"""

    printer_config : PrinterConfig = PrinterConfig()

    first_layer_config : LayerConfig = LayerConfig()
    default_layer_config : LayerConfig = LayerConfig()


    layers: List[Layer] = field(default_factory=list)


    next_layer_index: int = 0
    next_layer_bottom: float = 0


    def new_layer(self, layer_config: LayerConfig = None):
        if layer_config is None:
            if self.next_layer_index == 0:
                layer_config = self.first_layer_config
            else:
                layer_config = self.default_layer_config

        layer = Layer(layer_config, self.next_layer_index, self.next_layer_bottom)
        self.layers.append(layer)
        return layer







    def before_layer_change(self):
        pass

    def after_layer_change(self):
        pass

    def get_layer_by_index(self, index):
        pass

    def get_layers_by_index(self, start, end):
        pass

    def get_layers_by_height(self, bottom, top):
        pass


def test_move_config():
    print(MoveConfig())


if __name__ == "__main__":
    test_move_config()

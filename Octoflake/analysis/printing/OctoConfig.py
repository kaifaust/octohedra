import math

SQRT2 = math.sqrt(2)
SQRT22 = SQRT2 / 2


class OctoConfig:
    def __init__(self,
                 nozzle=0.4,
                 nozzle_width_multiplier=1.25,
                 line_layer_ratio=2,
                 overlap_ratio=1,
                 first_layer_multiplier=1,
                 layers_per_cell=None,
                 target_overlap_cell_ratio=5,
                 slit_ratio=0.001,
                 slit_absolute=None):
        self.nozzle = nozzle
        self.nozzle_width_multiplier = nozzle_width_multiplier
        self.line_layer_ratio = line_layer_ratio
        self.overlap_ratio = overlap_ratio
        self.first_layer_multiplier = first_layer_multiplier
        self.layers_per_cell = layers_per_cell
        self.target_overlap_cell_ratio = target_overlap_cell_ratio
        self.slit_ratio = slit_ratio
        self.slit_absolute = slit_absolute

        # Derived renderer parameters
        self.cell_size = None
        self.slit = None
        self.overlap = None
        self.floor = None

        # Derived slicer settings
        self.line_width = None
        self.layer_height = None
        self.solid_layers = None

        self.derive()

    def derive(self):
        line_width = round(self.nozzle * self.nozzle_width_multiplier, 3)
        layer_height = round(line_width / self.line_layer_ratio, 3)
        slit = self.slit_absolute if self.slit_absolute is not None else line_width * self.slit_ratio

        overlap = slit + line_width + (1 - self.overlap_ratio) * line_width * (SQRT2 - 1) + 0.0001

        target_cell_size = 1 * self.target_overlap_cell_ratio * overlap
        target_layers = math.ceil(target_cell_size * SQRT22 / layer_height)
        layers = self.layers_per_cell if self.layers_per_cell is not None else target_layers
        cell_size = layers * layer_height / SQRT22
        target_floor = overlap / 2
        first_layer_height = layer_height * self.first_layer_multiplier

        solid_layers = 1 + round((target_floor - first_layer_height * layer_height) / layer_height)

        floor = first_layer_height + (solid_layers - 1) * layer_height

        print("\nSettings")
        print("Line width:", line_width)
        print("Layer height:", layer_height)
        print("First layer multiplier:", self.first_layer_multiplier)
        print("Solid Layers:", solid_layers)

        print("\nOther stats")
        print("Layers per cell:", layers)
        print("First layer height:", first_layer_height)
        print("Floor thickness:", floor)
        print("Cell Size:", cell_size)
        print("Overlap:", overlap)
        print("size/overlap:", cell_size / overlap)

        self.cell_size = cell_size
        self.overlap = overlap
        self.slit = slit
        self.floor = floor

        return self

    # def __setattr__(self, name, value):
    #     super.__setattr__(name, value)
    #     self.derive()

    def print_settings(self):
        print("\nSettings")
        print("Line width:", self.line_width)
        print("Layer height:", self.layer_height)
        print("First layer multiplier:", self.first_layer_multiplier)
        print("Solid Layers:", self.solid_layers)

    def file_name(self):
        return f""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.cell_size=}, {self.overlap=}, {self.slit=}, {self.floor=}"


if __name__ == "__main__":
    print("hello")
    gen = OctoConfigGenerator()
    print(gen.generate())

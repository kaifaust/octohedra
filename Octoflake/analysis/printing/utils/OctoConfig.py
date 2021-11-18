import math
from dataclasses import dataclass
from numbers import Real

from printing.utils.OctoUtil import SQRT2, SQRT22

OVERLAP_EPS = 0.0001


# class OctoConfig:
#     def __init__(self, cell_size=2, overlap=.25, slit=0.001):
#         self.cell_size = cell_size  # Note that this is the diagonal
#         self.overlap = overlap
#         self.slit = slit
#
#     def __repr__(self):
#         return f"OctoConfig(cell_size={self.cell_size:.5f}, overlap={self.overlap:.5f}, " \
#                f"slit={self.slit:.5f})"


# floor_height
#         overlap = config.overlap
#         oversize = config.cell_size + overlap
#         slit = config.slit

# @dataclass
# class PrintConfig:
#     cell_size: Real
#     overlap: Real
#     slit: Real
#     floor: Real


class OctoConfig:
    def __init__(self,
                 name="Unnamed",
                 nozzle=0.4,
                 nozzle_width_multiplier=1.25,
                 absolute_line_width=None,
                 line_layer_ratio=2,
                 absolute_layer_height=None,
                 first_layer_multiplier=1,
                 target_overlap_cell_ratio=5,
                 absolute_layers_per_cell=None,
                 absolute_overlap=None,
                 line_overlap=1,
                 slit_ratio=0.001,
                 absolute_slit=None,
                 decimals=5,
                 solid_layers=1,
                 **settings
                 ):

        self.name = name
        self.nozzle = nozzle
        self.nozzle_width_multiplier = nozzle_width_multiplier
        self.absolute_line_width = absolute_line_width
        self.line_layer_ratio = line_layer_ratio
        self.absolute_layer_height = absolute_layer_height
        self.first_layer_multiplier = first_layer_multiplier
        self.target_overlap_cell_ratio = target_overlap_cell_ratio
        self.absolute_layers_per_cell = absolute_layers_per_cell
        self.absolute_overlap = absolute_overlap
        self.line_overlap = line_overlap
        self.slit_ratio = slit_ratio
        self.slit_absolute = absolute_slit

        self.decimals = decimals
        self.settings = settings

        self.line_width = None
        self.layer_height = None

        self.cell_size = None
        self.overlap = None
        self.slit = None
        self.layers_per_cell = None
        self.first_layer_height = None
        self.solid_layers = solid_layers
        self.floor_height = None

        self.derive()

    def derive(self):

        self.line_width = self.nozzle * self.nozzle_width_multiplier \
            if self.absolute_line_width is None else self.absolute_line_width

        self.line_width = round(self.line_width, self.decimals)

        self.layer_height = self.line_width / self.line_layer_ratio \
            if self.absolute_layer_height is None else self.absolute_layer_height

        self.layer_height = round(self.layer_height, self.decimals)

        self.first_layer_height = self.layer_height * self.first_layer_multiplier

        self.slit = self.line_width * self.slit_ratio \
            if self.slit_absolute is None \
            else self.slit_absolute

        # TODO: This is gross. Work in the SQRT
        computed_overlap = \
            self.line_width \
            + (1 - self.line_overlap) * self.line_width * (SQRT2 - 1) \
            + OVERLAP_EPS

        self.overlap = computed_overlap * SQRT2 if not \
            self.absolute_overlap \
            else self.absolute_overlap

        # self.overlap *= SQRT2

        target_cell_size = self.target_overlap_cell_ratio * self.overlap
        target_layers = math.ceil(target_cell_size * SQRT22 / self.layer_height)

        self.layers_per_cell = target_layers if self.absolute_layers_per_cell is None else \
            self.absolute_layers_per_cell

        self.cell_size = 2 * self.layers_per_cell * self.layer_height  # / SQRT22

        self.floor_height = self.first_layer_height + (self.solid_layers - 1) * self.layer_height

        # print(self.overlap, self.overlap/2, self.first_layer_height, self.layer_height,
        # self.solid_layers)

    def print_derived_values(self):
        print("\nOther stats")
        print("Layers per cell:", self.layers_per_cell)
        print("First layer height:", self.first_layer_height)
        print("Cell Size:", self.cell_size)
        print("Overlap:", self.overlap)
        print("size/overlap:", self.cell_size / self.overlap)

    def print_settings(self):

        print("\nSettings")
        print("Line width:", self.line_width)
        print("Layer height:", self.layer_height)
        print("First layer multiplier:", self.first_layer_multiplier)
        print("Solid Layers:", self.solid_layers)
        for setting, value in self.settings.items():
            print(f"{setting}: {value}")

    def __str__(self):
        return self.name

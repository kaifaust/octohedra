import math
from dataclasses import dataclass, field
from functools import wraps
from numbers import Real

from printing.utils.OctoUtil import SQRT2, SQRT22

OVERLAP_EPS = 0.0001  # Needed to ensure the slicer generates a contiguous perimeter
DECIMALS = 7  # Ensure that settings needed to be punched into the slicer aren't arbitrarily long


@dataclass(frozen=True)
class RenderConfig:
    """This class holds only the values that are ultimately relevant to the rendering process,
    leaving out parts of the config that are only relevant to the slicing/printing phase.
    """
    cell_size: Real
    overlap: Real
    slit: Real
    floor_height: Real
    first_layer_height: Real
    layer_height: Real
    line_width: Real


# Decorator to makes a method into a property getter that rounds its output
def rounded_property(method, n=DECIMALS) -> property:
    @wraps(method)
    def wrapper(self):
        return round(method(self), n)

    return property(wrapper)


@dataclass
class OctoConfig:
    """Contains/derives all the information needed to render and print an OctoGrid. All
    measurements in mm.

    Can accept various parameters for how the various values relate to each other, or you can
    provide the 'absolute_xxx' versions to supply your pre-determined values.

    first_layer_multiplier - This should be .5, 1.5, 2.5 etc, if you want the equators of the
    octahedrons to be sharp. Setting this to an integer will result in layers equally spaced above
    and below the equator, rather than right on it.

    target_cell_width - Use this if you are trying to ensure that the rendered OctoGrid will fit
    on your printer build plate. OctoConfig will round down so as to chose a value for
    layers_per_cell that ensures the cells are smaller than or equal to the target width. Takes
    precedence over target_overlap_cell_ratio (but is overridden by absolute_layers_per_cell).

    target_overlap_cell_ratio - Use this this value to control how distinct the smallest
    octahedrons are from each other. A value of 5 or higher generally looks good, while 3 is
    about the smallest value with acceptable aesthetics. Values below 2 would cause the smallest
    octahedrons to merge, and are thus not allowed. OctoConfig will round up so as to chose a
    value for layers_per_cell that exceeds the target ratio.

    settings - Use to record printer settings that are not related to geometry, such as
    temperature and speed.
    """

    name: str = "Unnamed OctoConfig"

    nozzle_width: float = 0.4
    nozzle_width_multiplier: float = 1.25
    absolute_line_width: float = None

    line_layer_ratio: float = 2.0
    absolute_layer_height: float = None

    first_layer_multiplier: float = 1.5
    absolute_first_layer_height: Real = None

    solid_layers: int = 2
    absolute_floor_height: float = None

    slit_ratio: float = 0.001
    absolute_slit: float = 0.01  # TODO: Clean this up

    line_overlap: float = 1.0
    absolute_overlap: float = None

    target_overlap_cell_ratio: float = 5.0
    target_cell_width: float = None
    absolute_layers_per_cell: int = None

    settings: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.target_overlap_cell_ratio is not None:
            if self.target_overlap_cell_ratio < 2:
                raise ValueError("A target cell size/overlap ratio of <2 doesn't work")

    def derive_render_config(self):

        # if self.overlap >= self.cell_size / 2:
        #     raise ValueError("Overlap busted")  # TODO: Better message here

        # TODO: Check that the slit and floor height aren't busted either

        return RenderConfig(self.cell_size,
                            self.overlap,
                            self.slit,
                            self.floor_height,
                            self.first_layer_height,
                            self.layer_height,
                            self.line_width)

    @rounded_property
    def line_width(self):
        if self.absolute_line_width is not None:
            return self.absolute_line_width
        else:
            return self.nozzle_width * self.nozzle_width_multiplier

    @rounded_property
    def layer_height(self):
        if self.absolute_layer_height is not None:
            return self.absolute_layer_height
        else:
            return self.line_width / self.line_layer_ratio

    @rounded_property
    def first_layer_height(self):
        if self.absolute_first_layer_height is not None:
            return self.absolute_first_layer_height
        else:
            return self.layer_height * self.first_layer_multiplier

    @rounded_property
    def floor_height(self):
        if self.absolute_floor_height is not None:
            return self.absolute_floor_height
        else:
            return self.layer_height # TODO

    @property
    def floor_layers(self):
        return math.floor((self.floor_height - self.first_layer_height) / self.layer_height)

    @rounded_property
    def slit(self):
        if self.absolute_slit is not None:
            return self.absolute_slit
        else:
            return self.line_width * self.slit_ratio

    @rounded_property
    def overlap(self):
        if self.absolute_overlap is not None:
            return self.absolute_overlap
        else:
            computed_overlap = \
                self.line_width \
                + (1 - self.line_overlap) * self.line_width * (SQRT2 - 1) \
                + OVERLAP_EPS
            return computed_overlap * SQRT2 # TODO: Wat

    @property
    def layers_per_cell(self):
        """Note that this is actually the number of layers you have to add, starting from one
        equator, to get to the next equator up.
        """

        if self.absolute_layers_per_cell is not None:
            return self.absolute_layers_per_cell
        elif self.target_cell_width is not None:
            print(self.target_cell_width, self.layer_height)

            return math.floor(self.target_cell_width * SQRT22 / self.layer_height)
        else:
            target_cell_size = self.target_overlap_cell_ratio * self.overlap
            # print(target_cell_size)
            layers = math.ceil(target_cell_size /2 / self.layer_height)
            # print(target_cell_size, target_cell_size /2, self.layer_height, layers)
            return layers

    @rounded_property
    def cell_size(self):
        """The point-to-opposite-point size of the octahedrons, neglecting overlap."""
        return 2 * self.layers_per_cell * self.layer_height

    def print_derived_values(self):
        print("\nOther stats")
        print("\tLayers per cell:", self.layers_per_cell)
        print("\tFirst layer height:", self.first_layer_height)
        print("\tCell Size:", self.cell_size)
        print("\tOverlap:", self.overlap)
        print("\tSize/Overlap:", self.cell_size / self.overlap)

    def print_settings(self):

        print("\nSettings")
        print("\tLine width:", self.line_width)
        print("\tLayer height:", self.layer_height)
        print("\tFirst layer multiplier:", self.first_layer_multiplier)
        print("\tFloor layers:", self.floor_layers)
        for setting, value in self.settings.items():
            print(f"{setting}: {value}")

    def __str__(self):
        return self.name

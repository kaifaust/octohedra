from math import sqrt

from printing.utils.OctoConfig import OctoConfig

default = config_20 = OctoConfig(
        name="0.2mm",
        nozzle_width=0.2,
        absolute_line_width=.26,
        line_layer_ratio=2,
        absolute_layers_per_cell=8,
        line_overlap=.99,
        absolute_slit=.001
        )

config_20_thin = OctoConfig(
        name="0.2mm",
        nozzle_width=0.2,
        absolute_line_width=0.25,
        # line_layer_ratio=1.5,
        absolute_layer_height=0.10,
        # absolute_first_layer_height=0.199,
        absolute_first_layer_height=0.15,
        absolute_floor_height=.01,
        target_cell_width=1.5,
        line_overlap=.999,
        absolute_slit=.0001
        )





layer_height = 0.1
line_width =layer_height * 2 * sqrt(2)

config_20_thin_cont = OctoConfig(
        name="",
        nozzle_width=0.2,
        # absolute_line_width=0.25, # * sqrt(2),
        absolute_line_width=line_width/2,
        # absolute_line_width=0.2,

        # line_layer_ratio=1.5,
        absolute_layer_height=layer_height,
        absolute_overlap=4 * layer_height,
        # absolute_layer_height=0.2 /3 * sqrt(2),
        # absolute_layer_height=0.095,
        absolute_first_layer_height=0.199,
        absolute_floor_height=.01,
        target_cell_width=1.5,
        # line_overlap=.99,
        absolute_slit=.001
        )


# .24, .08 getting too much drag and just inconsistent extrusion amounts



config_25 = OctoConfig(
        name="0.25mm",
        nozzle_width=0.25,
        absolute_line_width=0.3,
        absolute_layer_height=0.15,
        absolute_floor_height=0.01,
        absolute_first_layer_height=0.19,
        target_cell_width=1,
        line_overlap=0.99,
        absolute_slit=0.001
        )

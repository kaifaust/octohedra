import math

from printing.octo.OctoConfig import PrinterOctoConfigBuilder, OctoConfig

render_testing = OctoConfig(10, 3, 0.1)
no_overlap = OctoConfig(10, 0, 0)

# config_2 = PrinterOctoConfigBuilder(
#     nozzle=0.2,
#     nozzle_width_multiplier=1.3,  # * 0.25 / 0.2,
#     line_layer_ratio=2,
#     first_layer_multiplier=0.5,
#     absolute_layers_per_cell=8,
# )
#
# Best so far
config_25 = PrinterOctoConfigBuilder(
    nozzle=0.25,
    nozzle_width_multiplier=1.3,
    line_layer_ratio=2,
    first_layer_multiplier=.5,
    absolute_layers_per_cell=8,
    absolute_slit=0.001
)
#
# config_3 = PrinterOctoConfigBuilder(
#     nozzle=0.3,
#     nozzle_width_multiplier=1,
#     line_layer_ratio=math.sqrt(2),
#     first_layer_multiplier=.5,
#     absolute_layers_per_cell=5,
# )

config_3_thin = PrinterOctoConfigBuilder(
    nozzle=0.3,
    nozzle_width_multiplier=2,
    line_layer_ratio= 6,
    first_layer_multiplier=1.5,
    # absolute_layers_per_cell=20,
    line_overlap=1,
    target_overlap_cell_ratio=5,
    Speed=5,
    Temp=190
)

# config_4 = PrinterOctoConfigBuilder(
#     nozzle=0.4,
#     nozzle_width_multiplier=1.3,
#     line_layer_ratio=2,
#     first_layer_multiplier=.5,
#     absolute_layers_per_cell=8,
# )
#
# config_transparent_04 = PrinterOctoConfigBuilder(
#     nozzle=0.4,
#     nozzle_width_multiplier=1.1,
#     line_layer_ratio=1.5,
#     first_layer_multiplier=0.5,
#     absolute_layers_per_cell=16,
# )
#
config_8 = PrinterOctoConfigBuilder(
    nozzle=0.8,
    # nozzle_width_multiplier=1.3,  # .35/.25,
    absolute_line_width= 1,
    line_layer_ratio=2,
    first_layer_multiplier=1,
    absolute_layers_per_cell=8,
    line_overlap=1,
    absolute_slit=.001
)
#
# config_transparent_8 = PrinterOctoConfigBuilder(
#     nozzle=0.8,
#     nozzle_width_multiplier=1.3,  # .35/.25,
#     line_layer_ratio=2,
#     first_layer_multiplier=.5,
#     absolute_layers_per_cell=10,
#     line_overlap=1,
#     absolute_slit=.001
# )
#
# config_8_thin = PrinterOctoConfigBuilder(
#     nozzle=0.8,
#     nozzle_width_multiplier=.9,  # .35/.25,
#     line_layer_ratio=5,
#     first_layer_multiplier=.5,
#     absolute_layers_per_cell=20,
#     line_overlap=1,
#     absolute_slit=.001
# )

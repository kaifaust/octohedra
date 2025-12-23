from printing.utils.OctoConfig import OctoConfig

rainbow_gem_line_width = .32
rainbow_gem_layer_height = .12

config_20_rainbow_gem = OctoConfig(
        name="Rainbow Gem",
        nozzle_width=0.2,
        absolute_line_width=rainbow_gem_line_width,
        absolute_layer_height=rainbow_gem_layer_height,
        line_overlap=1,
        absolute_first_layer_height=.1999,
        absolute_floor_height=.01,
        absolute_layers_per_cell=12,
        target_cell_width=2,
        absolute_slit=.001
        )

default = config_20_rainbow_gem

rainbow_speed_line_width = .12
rainbow_speed_layer_height = .12

config_20_rainbow_speed = OctoConfig(
        name="Rainbow Speed",
        nozzle_width=0.2,
        absolute_line_width=rainbow_speed_line_width,
        absolute_layer_height=rainbow_speed_layer_height,
        line_overlap=1,
        absolute_first_layer_height=0.1999,
        absolute_floor_height=.5 * rainbow_speed_layer_height,
        target_cell_width=1,
        # absolute_layers_per_cell=10,
        absolute_slit=.01
        )

quantum_gem_line_width = .1
quantum_gem_layer_height = 0.1

config_20_quantum_gem = OctoConfig(
        name="Quantum Gem",
        nozzle_width=0.2,
        absolute_line_width=quantum_gem_line_width,
        absolute_layer_height=quantum_gem_layer_height,
        line_overlap=1,
        absolute_first_layer_height=0.199,
        absolute_floor_height=.01,
        target_cell_width=4,
        absolute_slit=.001
        )

quantum_speed_layer_height = 0.125
quantum_speed_line_width = 0.28

config_20_quantum_Speed = OctoConfig(
        name="Quantum Speed",
        nozzle_width=0.2,
        absolute_line_width=quantum_speed_line_width,
        absolute_layer_height=quantum_speed_layer_height,
        line_overlap=0.5,
        absolute_first_layer_height=.1999,
        absolute_floor_height=.01,
        target_cell_width=3,
        absolute_slit=.001
        )

##################### Debug shit

giant_debug = OctoConfig(
        name="Giant Debug",
        nozzle_width=2,
        absolute_line_width=2,
        absolute_layer_height=1,
        line_overlap=0,
        absolute_first_layer_height=1,
        absolute_floor_height=0.1,
        absolute_layers_per_cell=8,
        absolute_slit=0.001
        )

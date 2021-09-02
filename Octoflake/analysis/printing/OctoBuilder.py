import OctoGrid


class OctoBuilder:

    def __init__(self, iteration):
        self.iteration = iteration
        self.grid = OctoGrid()

    def tower(grid, iteration, center=(0, 0, 0)):
        z = center[2]
        for i in range(iteration, 0, -1):
            print(i)
            grid.make_flake(i, (center[0], center[1], center[2] + z))
            z += 2 ** i

    def tower_complex(grid, iteration, center=(0, 0, 0)):
        if iteration < 3:
            return
        tower(grid, iteration, center)
        tower_complex(grid, iteration - 1, (center[0] + 2 ** iteration, center[1] + 2 ** iteration, center[2]))
        tower_complex(grid, iteration - 1, (center[0] + 2 ** iteration, center[1] - 2 ** iteration, center[2]))
        tower_complex(grid, iteration - 1, (center[0] - 2 ** iteration, center[1] + 2 ** iteration, center[2]))
        tower_complex(grid, iteration - 1, (center[0] - 2 ** iteration, center[1] - 2 ** iteration, center[2]))

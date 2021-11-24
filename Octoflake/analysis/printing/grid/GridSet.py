from collections import defaultdict
from dataclasses import dataclass, field

from printing.grid.OctoGrid import OctoGrid

DEFAULT = "default"


class GridSet(OctoGrid):


    def __init__(self):
        self.grids = defaultdict(OctoGrid)
        self.grids[DEFAULT] = OctoGrid()

    def __getitem__(self, item):
        return self.grids[item]

    def keep_octo(self, m, center, apply_to_all=True):
        if apply_to_all:
            for grid in self.grids.values():
                grid.keep_octo(m, center)
        else:
            self.grids[DEFAULT].keep_octo(m, center)


if __name__ == '__main__':
    gs = GridSet()
    print(gs.grids)
    print(gs["object"])

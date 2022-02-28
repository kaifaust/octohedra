from printing.grid.OctoVector import OctoVector


class OctoLayers:

    def __init__(self, center:OctoVector, radius:int):
        self.center = center
        self.radius = radius


    def path(self, layer):

        r = self.radius - (self.radius - layer)

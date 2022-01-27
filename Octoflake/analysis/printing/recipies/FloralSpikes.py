import numpy as np
from trimesh.creation import cone

from printing.utils import RenderUtils

multiplier = 10
min_height = 15
max_height = 50

for radius in np.linspace(2, 5, 20):

    height = radius * multiplier
    height = min(max_height, height)
    height = max(min_height, height)

    mesh = cone(radius, height)
    RenderUtils.save_mesh(mesh, "cone", radius=radius)

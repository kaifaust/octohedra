from math import ceil, floor
from dataclasses import dataclass

import numpy as np
import trimesh.util
from shapely import linearrings, linestrings, polygons, Polygon
from trimesh.creation import sweep_polygon
from trimesh.exchange.export import export_mesh
from trimesh.intersections import slice_mesh_plane
from trimesh.primitives import Cylinder, Sphere, Box
from trimesh.transformations import translation_matrix
from trimesh.boolean import difference, union

from printing.utils.RenderUtils import save_mesh


# def coin_with_cylindrical_void(coin_radius,
#                                coin_thickness,
#                                void_radius,
#                                void_thickness,
#                                filename="CoinWithVoid",
#                                sections=200):
#     coin = Cylinder(radius=coin_radius, height=coin_thickness, center=[0, 0, 0], sections=sections)
#     void = Cylinder(radius=void_radius, height=void_thickness, center=[0, 0, 0], sections=sections)
#
#     # void.apply_transform(translation_matrix([0, 0, 1]))
#
#     coin_with_void = difference([coin, void])
#     save_mesh(coin_with_void, filename=filename)


@dataclass
class MyBox:
    """
    Makes a storage box!

    The dimensions represent the overall dimensions, including the rim at the top for stacking!


    """


    name: str = "Box"

    length: float = 100
    width: float = 70
    depth: float = 20

    wall_thickness: float = 2
    bottom_thickness: float = 3

    rim_thickness: float = wall_thickness
    rim_clearance: float = 0.5


    def build(self):
        outside = Box(extents=(self.length, self.width, self.depth))

        inside = Box(
            extents=(
                self.length - 2 * self.wall_thickness,
                self.width - 2 * self.wall_thickness,
                self.depth - self.bottom_thickness
            ),
            transform=translation_matrix([0, 0, self.bottom_thickness])
        )

        rim_profile = Polygon(((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)))
        polygon = rim_profile

        # print(np.array(polygon.exterior.coords))
        print(np.array(polygon.exterior.coords)[:-1])

        print(rim_profile.area)
        # exit()


        rim_path = np.array([[100, 100, 100], [200, 200, 200]])
        rim = sweep_polygon(rim_profile, rim_path)

        box = difference([outside, inside])
        box = union([box, rim])

        mesh = box
        save_mesh(mesh, filename=self.name)


if __name__ == "__main__":
    MyBox().build()

from math import ceil, floor
from dataclasses import dataclass

import trimesh.util
from trimesh.intersections import slice_mesh_plane
from trimesh.primitives import Cylinder, Sphere
from trimesh.transformations import translation_matrix
from trimesh.boolean import difference

from printing.utils.RenderUtils import save_mesh


def coin_with_cylindrical_void(coin_radius,
                               coin_thickness,
                               void_radius,
                               void_thickness,
                               filename="coinwithvoid",
                               sections=200):
    coin = Cylinder(radius=coin_radius, height=coin_thickness, center=[0, 0, 0], sections=sections)
    void = Cylinder(radius=void_radius, height=void_thickness, center=[0, 0, 0], sections=sections)

    # void.apply_transform(translation_matrix([0, 0, 1]))

    coin_with_void = difference([coin, void])
    save_mesh(coin_with_void, filename=filename)


@dataclass
class Magnet:
    name: str
    nominal_diameter: float
    nominal_height: float
    horizontal_clearance: float = 0.05
    vertical_clearance: float = 0.04


def generate_test_coins():
    print("Generating test riffle tokens")



    layer_height = .2
    layer_count = 17

    coin_radius = 20
    coin_thickness = layer_count * layer_height

    sections = 100

    magnets = [
        Magnet("2x1", 2, 1, .1),
        Magnet("Double 2x1", 2, 2, .1),
        Magnet("3x1", 3, 1),
        Magnet("Double 3x1", 3, 2),
        Magnet("4x2", 4, 2)
        ]

    for magnet in magnets:
        magnet_layers = ceil(
                (magnet.nominal_height + magnet.vertical_clearance) / layer_height
                )

        void_radius = magnet.nominal_diameter/2 + magnet.horizontal_clearance
        void_thickness = magnet_layers * layer_height

        layers_below = floor((layer_count-magnet_layers)/2)
        void_center_height = layers_below * layer_height + void_thickness/2

        print(magnet.name, magnet_layers, layers_below)

        coin = Cylinder(radius=coin_radius,
                        height=coin_thickness,
                        center=[0, 0, coin_thickness/2],
                        sections=sections)
        void = Cylinder(radius=void_radius,
                        height=void_thickness,
                        center=[0, 0, void_center_height],
                        sections=sections)

        # void.apply_transform(translation_matrix([0, 0, 1]))

        coin_with_void = difference([coin, void])
        save_mesh(coin_with_void, filename=magnet.name)

        # coin_with_cylindrical_void()


if __name__ == '__main__':
    generate_test_coins()

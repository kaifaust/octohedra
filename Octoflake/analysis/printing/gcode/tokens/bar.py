from math import sqrt

import trimesh.util
from trimesh.intersections import slice_mesh_plane
from trimesh.primitives import Cylinder, Sphere
from trimesh.transformations import translation_matrix
from trimesh.boolean import difference

from printing.utils.RenderUtils import save_mesh


def make_bar(length=50, width=25, thickness=3.5, radius=5, filename="bar"):
    corner = Cylinder(radius=radius, height=thickness)  # , sections = 60)
    x_shift = width / 2 - radius
    y_shift = length / 2 - radius
    mesh1 = corner.copy().apply_transform(translation_matrix([-x_shift, -y_shift, 0]))
    mesh2 = corner.copy().apply_transform(translation_matrix([x_shift, -y_shift, 0]))
    mesh3 = corner.copy().apply_transform(translation_matrix([x_shift, y_shift, 0]))
    mesh4 = corner.copy().apply_transform(translation_matrix([-x_shift, y_shift, 0]))
    void1 = Cylinder(radius=7.5, height=1.7, transform=translation_matrix([0, 0, 0]))
    void2 = Cylinder(radius=3, height=1.7, transform=translation_matrix([0, -15, 0]))
    void3 = Cylinder(radius=3, height=1.7, transform=translation_matrix([0, 15, 0]))

    bar = trimesh.util.concatenate([mesh1, mesh2, mesh3, mesh4]).convex_hull
    bar_with_voids = difference([bar, void1, void2, void3])
    save_mesh(bar, filename=filename)
    save_mesh(bar_with_voids, filename="Bar with voids")


def make_plaque(length=55 * 1.618, width=55, thickness=7, radius=4, filename="plaque"):
    corner1 = Sphere(radius=radius, center=[radius, radius, 0], subdivisions=4)
    corner2 = Sphere(radius=radius, center=[width - radius, radius, 0], subdivisions=4)
    corner3 = Sphere(radius=radius, center=[radius, length - radius, 0], subdivisions=4)
    corner4 = Sphere(radius=radius, center=[width - radius, length - radius, 0], subdivisions=4)
    plaque = trimesh.util.concatenate([corner1, corner2, corner3, corner4])

    plaque = slice_mesh_plane(plaque, plane_normal=[0, 0, -1], plane_origin=[0, 0, thickness / 2])
    plaque = slice_mesh_plane(plaque, plane_normal=[0, 0, 1], plane_origin=[0, 0, -thickness / 2])

    save_mesh(plaque.convex_hull, filename=filename)


# def make_plaque_fancy(length=55 * 1.618, width=55, thickness=7, radius=4, curve_radius=10,
# filename="plaque"):
#     corner = Cylinder(radius=curve_radius, height=thickness, sections=60)
#     mesh1 = corner.copy().apply_transform(translation_matrix([radius, radius, 0]))
#     mesh2 = corner.copy().apply_transform(translation_matrix([width - radius, radius, 0]))
#     mesh3 = corner.copy().apply_transform(translation_matrix([radius, length - radius, 0]))
#     mesh4 = corner.copy().apply_transform(translation_matrix([width - radius, length - radius,
#     0]))
#
#     curve = mesh_plane(Sphere(radius=radius, center=[0, 0, 0], subdivisions=4),
#                        plane_normal=[0, 1, 0],
#                        plane_origin=[0, 0, 0])
#
#
#     # corner2 = Sphere(radius=radius, center=[width - radius, radius, 0], subdivisions=4)
#     # corner3 = Sphere(radius=radius, center=[radius, length - radius, 0], subdivisions=4)
#     # corner4 = Sphere(radius=radius, center=[width - radius, length - radius, 0], subdivisions=4)
#
#     plaque = trimesh.util.concatenate([mesh1, mesh2, mesh3, mesh4])
#
#     outline = mesh_plane(plaque, plane_normal=[0, 0, 1], plane_origin=[0, 0, 0])
#
#     print(outline)
#
#     print(Polygon(curve))
#
#
#     plaque = slice_mesh_plane(plaque, plane_normal=[0, 0, -1], plane_origin=[0, 0, thickness / 2])
#     plaque = slice_mesh_plane(plaque, plane_normal=[0, 0, 1], plane_origin=[0, 0, -thickness / 2])
#
#     save_mesh(plaque.convex_hull, filename=filename)


def make_coin(radius=20, thickness=3.5, filename="coin"):
    save_mesh(Cylinder(radius=radius, height=thickness, sections=300), filename=filename)


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


def bar_for_mini_magnet():
    length = 22.5
    width = 12.5
    thickness = 3.5
    corner_radius = 2.5

    magnet_length = 10
    magnet_width = 4
    magnet_thickness = 2

    # corner = Cylinder(radius=corner_radius, height=thickness)  # , sections = 60)
    x_shift = width / 2 - corner_radius
    y_shift = length / 2 - corner_radius

    # noinspection PyTypeChecker
    bar = trimesh.util.concatenate((
        Cylinder(radius=corner_radius,
                 height=thickness,
                 transform=translation_matrix([-x_shift, -y_shift, 0])),
        Cylinder(radius=corner_radius,
                 height=thickness,
                 transform=translation_matrix([x_shift, y_shift, 0])),
        Cylinder(radius=corner_radius,
                 height=thickness,
                 transform=translation_matrix([x_shift, -y_shift, 0])),
        Cylinder(radius=corner_radius,
                 height=thickness,
                 transform=translation_matrix([-x_shift, y_shift, 0])),
        )).convex_hull

    void = trimesh.primitives.Box(extents=[magnet_width, magnet_length, magnet_thickness])

    # corner.copy().apply_transform(translation_matrix([-x_shift, -y_shift, 0]))
    # mesh2 = corner.copy().apply_transform(translation_matrix([x_shift, -y_shift, 0]))
    # mesh3 = corner.copy().apply_transform(translation_matrix([x_shift, y_shift, 0]))
    # mesh4 = corner.copy().apply_transform(translation_matrix([-x_shift, y_shift, 0]))
    # void1 = Cylinder(radius=7.5, height=1.7, transform = translation_matrix([0, 0, 0]))
    # void2 = Cylinder(radius=3, height=1.7, transform = translation_matrix([0, -15, 0]))
    # void3 = Cylinder(radius=3, height=1.7, transform = translation_matrix([0, 15, 0]))
    #
    # bar = trimesh.util.concatenate([mesh1, mesh2, mesh3, mesh4]).convex_hull
    # bar_with_voids = difference([bar, void1, void2, void3])
    # save_mesh(bar, filename=filename)
    # save_mesh(bar_with_voids, filename="Bar with voids")
    #

    save_mesh(bar, filename="Mini bar")
    save_mesh(difference([bar, void]), "Mini magnet bar")


if __name__ == "__main__":
    bar_for_mini_magnet()

    # for void_radius in (6, 8, 10, 12, 15):
    #     coin_with_cylindrical_void(20, 3.5, void_radius/2, 1.725,f"coin with {void_radius}")

    # void_radius = 8
    # coin_with_cylindrical_void(5, 3.5, void_radius/2, 1.7,f"speck with 6mm void")
    # void_radius = 15
    # coin_with_cylindrical_void(20, 3.5, void_radius / 2, 1.7, f"bit")
    #
    thickness = 3.5
    # make_coin(0.4645 * 20, thickness, filename="tidbit")
    make_coin(10, thickness, filename="bit")
    # make_coin(20 / (1 + sqrt(2)), thickness, filename="bit")
    # make_coin(10, thickness, filename="nibble")

    # make_bar(45, 25, thickness, 5, "stubby_bar")

    # make_bar(45 / 2, 25 / 2, thickness, 5 / 2, "tiny_bar")

    # make_plaque()
    # make_plaque_fancy()

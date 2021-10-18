from pathlib import Path

from stl import Mode, Mesh
import numpy as np

from printing.octo.OctoConfig import OctoConfig


# from printing.rendering.StlRenderer import StlRenderer
#
#
# def basic_render(grid, config=None, filename="derp.stl", base_path=None, z_min=0, mode=Mode.BINARY):
#     grid.compute_trimming()
#     grid.crop(z_min=z_min)
#
#     config = config if config is not None else OctoConfig()
#     renderer = StlRenderer()
#     base_path = base_path if base_path is not None else Path.home() / "Desktop"
#
#     path = base_path / filename
#
#     print(f"Rendering a grid with {len(grid.occ)} octos.")
#     print(f"Using {config}.")
#     mesh = renderer.render(config, grid)
#
#     print(f"Saving as {path}")
#     mesh.save(path, mode=mode)


def save_meshes(*meshes, filename="derp.stl", base_path=None, mode=Mode.BINARY):
    print(meshes)
    mesh_data = [mesh.data for mesh in meshes]
    mesh = Mesh(np.concatenate(mesh_data))
    base_path = base_path if base_path is not None else Path.home() / "Desktop"
    path = base_path / filename
    print(f"Saving mesh as {path}")
    mesh.save(path, mode=mode)
    print(f"Done!")


def stitch_belt_to_point(point, belt, is_bottom=False):
    faces = np.array([
        [belt[0], belt[1], point],
        [belt[1], belt[2], point],
        [belt[2], belt[3], point],
        [belt[3], belt[0], point],
    ])

    if is_bottom:
        faces = np.flip(faces, 1)

    return faces


def stitch_belts(top_belt, bottom_belt):
    assert len(top_belt) == len(bottom_belt)

    return np.concatenate([
        np.array([
            [bottom_belt[i - 1], bottom_belt[i], top_belt[i - 1]],
            [bottom_belt[i], top_belt[i], top_belt[i - 1]]
        ])

        for i in range(len(top_belt))
    ])

    # return np.array([
    #     [bottom_belt[0], bottom_belt[1], top_belt[0]],
    #     [bottom_belt[1], bottom_belt[2], top_belt[1]],
    #     [bottom_belt[2], bottom_belt[3], top_belt[2]],
    #     [bottom_belt[3], bottom_belt[0], top_belt[3]],
    #
    #     [bottom_belt[1], top_belt[1], top_belt[0]],
    #     [bottom_belt[2], top_belt[2], top_belt[1]],
    #     [bottom_belt[3], top_belt[3], top_belt[2]],
    #     [bottom_belt[0], top_belt[0], top_belt[3]],
    # ])


def seal_belt(belt, is_bottom=False):
    faces = np.array([
        [belt[0], belt[1], belt[2]],
        [belt[0], belt[2], belt[3]],
    ])

    if is_bottom:
        faces = np.flip(faces, 1)

    return faces


def testing():
    top_belt = [1, 2, 3]
    bottom_belt = ["a", "b", "c"]
    print(stitch_belts(top_belt, bottom_belt))


if __name__ == "__main__":
    testing()

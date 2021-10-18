import numpy as np
from euclid3 import Vector3
from stl import Mesh

from printing.octo.OctoCell import OctoCell
from printing.octo.OctoGrid import OctoGrid
from printing.rendering import RenderUtils


class TetraCell:
    """
    This is a tetrahedral cell in the tetra-octa honeycomb
    """

    def __init__(self):
        pass

    def render(self, center: Vector3, to_slopes_up=False, cell_size=10):
        x, y, z = tuple(center)
        center_arr = np.array(tuple(center))

        print(x, y, z, x - y + z % 2)

        if x - y + z % 2 == 0:
            b1 = Vector3(-1, -1, -1) * cell_size
            b2 = Vector3(1, 1, -1) * cell_size

            t2 = Vector3(1, -1, 1) * cell_size
            t1 = Vector3(-1, 1, 1) * cell_size

        else:
            b1 = Vector3(1, -1, -1) * cell_size
            b2 = Vector3(-1, 1, -1) * cell_size

            t2 = Vector3(1, 1, 1) * cell_size
            t1 = Vector3(-1, -1, 1) * cell_size

        faces = np.array([
            [b1, b2, t2],
            [b2, b1, t1],
            [t2, b2, t1],
            [t1, b1, t2]
        ])

        # print(faces)

        face_array = faces  # np.concatenate(faces)

        mesh = Mesh(np.zeros(face_array.shape[0], dtype=Mesh.dtype))
        mesh.vectors = face_array
        mesh.update_normals()
        print(center * cell_size)
        mesh.translate(center * cell_size)  # /SQRT2)

        # Todo, scale

        return mesh


def testing():
    tetra = TetraCell()

    mesh1 = tetra.render(Vector3(1, 1, 1))
    mesh2 = tetra.render(Vector3(1, -1, 3), to_slopes_up=True)

    # octo1 = OctoCell().render()

    RenderUtils.save_meshes(mesh1, mesh2)


if __name__ == "__main__":
    testing()

import numpy as np
from euclid3 import Vector3
from stl import Mesh

from printing.octo.OctoConfig import OctoConfig
from printing.octo.OctoUtil import DOWN, E, N, S, SQRT2, SQRT22, SQRT32, UP, W
from printing.rendering import RenderUtils


class TetraCell:
    """
    This is a tetrahedral cell in the tetra-octa honeycomb
    """

    def __init__(self):
        self.is_dummy = False


    def render(self, config:OctoConfig, center: Vector3):
        x, y, z = tuple(center)
        center_arr = np.array(tuple(center))
        spacing = config.cell_size/4
        overlap = config.overlap

        print(x, y, z, x - y + z % 2)

        tetra_size = spacing  + config.overlap/2 # SQRT2/4 *  (config.cell_size)
        tetra_scooch = overlap /2
        if x - y + z % 2 == 1:

            b1 = Vector3(-1, -1, -1) * tetra_size + tetra_scooch * (N + E + 2 * UP)
            b2 = Vector3(1, 1, -1) * tetra_size + tetra_scooch * (S + W + 2 * UP)

            t2 = Vector3(1, -1, 1) * tetra_size + tetra_scooch * (N + W)
            t1 = Vector3(-1, 1, 1) * tetra_size + tetra_scooch * (S + E)

        else:
            b1 = Vector3(1, -1, -1) * tetra_size
            b2 = Vector3(-1, 1, -1) * tetra_size

            t2 = Vector3(1, 1, 1) * tetra_size
            t1 = Vector3(-1, -1, 1) * tetra_size


        ba = b1



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
        center = Vector3(*center)
        print(center)
        print(tetra_size)
        print(spacing)
        print(center * spacing)
        mesh.translate(center * spacing)  # /SQRT2)

        # Todo, scale

        return mesh


def single_cell_testing():
    tetra = TetraCell()

    mesh1 = tetra.render(Vector3(1, 1, 1))
    mesh2 = tetra.render(Vector3(1, -1, 3), to_slopes_up=True)

    # octo1 = OctoCell().render()

    RenderUtils.save_meshes(mesh1, mesh2)


if __name__ == "__main__":
    single_cell_testing()

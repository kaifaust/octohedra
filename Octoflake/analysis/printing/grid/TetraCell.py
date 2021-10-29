import numpy as np
from euclid3 import Vector3
from stl import Mesh

from printing.grid.GridCell import GridCell, seal_belt, stitch_belts
from printing.grid.OctoCell import Trim
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoUtil import E, N, S, W


class TetraCell(GridCell):
    """
    This is a tetrahedral cell in the tetra-octa honeycomb
    """

    def __init__(self):
        super().__init__()

    # TODO: Make a render config that decouples the printer config details from the geometry
    def render(self, config, center):

        x = center.x
        y = center.y
        z = center.z

        spacing = config.cell_size / 4
        overlap = config.overlap
        tetra_size = config.cell_size / 4 + config.overlap / 2

        # start by assuming that the SW->NE line is on bottom
        bsw = Vector3(-1, -1, -1) * tetra_size
        bne = Vector3(1, 1, -1) * tetra_size

        tnw = Vector3(-1, 1, 1) * tetra_size
        tse = Vector3(1, -1, 1) * tetra_size

        # TODO: Add another belt so there aren't overlapping faces?
        top_belt = [
            tnw + overlap / 2 * Vector3(1, 0, -1),
            tnw + overlap / 2 * Vector3(0, -1, -1),
            tse + overlap / 2 * Vector3(-1, 0, -1),
            tse + overlap / 2 * Vector3(0, 1, -1),
            ]

        top_bottom_belt = [
            tnw + overlap * Vector3(1, 0, -1),
            tnw + overlap * Vector3(0, -1, -1),
            tse + overlap * Vector3(-1, 0, -1),
            tse + overlap * Vector3(0, 1, -1),
            ]

        bottom_belt = [
            bne + overlap / 2 * Vector3(-1, 0, 1),
            bsw + overlap / 2 * Vector3(0, 1, 1),
            bsw + overlap / 2 * Vector3(1, 0, 1),
            bne + overlap / 2 * Vector3(0, -1, 1),

            ]

        bottom_top_belt = [
            bne + overlap * Vector3(-1, 0, 1),
            bsw + overlap * Vector3(0, 1, 1),
            bsw + overlap * Vector3(1, 0, 1),
            bne + overlap * Vector3(0, -1, 1),

            ]

        slit = config.slit
        trim = (overlap + slit / 2) / 2

        if Trim.NE in self.trims:
            bottom_belt[0] -= (N + E) * trim / 2
            bottom_belt[3] -= (N + E) * trim / 2
        if Trim.NW in self.trims:
            top_belt[0] -= (N + W) * trim / 2
            top_belt[1] -= (N + W) * trim / 2
        if Trim.SW in self.trims:
            bottom_belt[1] -= (S + W) * trim / 2
            bottom_belt[2] -= (S + W) * trim / 2
        if Trim.SE in self.trims:
            top_belt[2] -= (S + E) * trim / 2
            top_belt[3] -= (S + E) * trim / 2

        faces = [seal_belt(top_belt),
                 stitch_belts(top_belt, top_bottom_belt),
                 stitch_belts(top_bottom_belt, bottom_top_belt),
                 stitch_belts(bottom_top_belt, bottom_belt),
                 seal_belt(bottom_belt, is_bottom=True)
                 ]

        face_array = np.concatenate(faces)

        if (x + y + z) % 4 == 1:
            face_array = face_array * np.array((1, 1, -1))
            face_array = np.flip(face_array, 1)

        mesh = Mesh(np.zeros(face_array.shape[0], dtype=Mesh.dtype))
        mesh.vectors = face_array
        mesh.update_normals()


        mesh.translate(center.to_np() * spacing)

        return mesh


def single_cell_testing():
    tetra = TetraCell()

    config = OctoConfigs.config_25
    mesh1 = tetra.render(config, Vector3(1, 1, 1))
    mesh2 = tetra.render(config, Vector3(1, 1, -1))

    # octo1 = OctoCell().render()

    RenderUtils.save_meshes(mesh1, mesh2)


if __name__ == "__main__":
    single_cell_testing()

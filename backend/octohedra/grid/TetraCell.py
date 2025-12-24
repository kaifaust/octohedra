from dataclasses import dataclass

import numpy as np
from euclid3 import Vector3

from octohedra.grid.GridCell import GridCell, belts_to_trimesh
from octohedra.grid.OctoVector import OctoVector
from octohedra.utils import OctoConfigs
from octohedra.utils.OctoUtil import NE, NW, SE, SW, E, N, S, W, Z


@dataclass
class TetraCell(GridCell):
    """
    This is a tetrahedral cell in the tetra-octa honeycomb
    """

    trim_ne: bool = False
    trim_nw: bool = False
    trim_sw: bool = False
    trim_se: bool = False
    flip: bool = False

    def trim(self, center: OctoVector, occ=set[OctoVector]):
        flip = 1 if (center.x + center.y + center.z) % 4 == 3 else -1
        o_wsw = center + -Z * flip + SW + 2 * W
        o_ssw = (center + -Z * flip + SW + 2 * S)
        o_ese = (center + Z * flip + SE + 2 * E)
        o_sse = (center + Z * flip + SE + 2 * S)
        o_wnw = (center + Z * flip + NW + 2 * W)
        o_nnw = (center + Z * flip + NW + 2 * N)
        o_ene = (center + -Z * flip + NE + 2 * E)
        o_nne = (center + -Z * flip + NE + 2 * N)

        self.trim_sw = o_wsw in occ or o_ssw in occ
        self.trim_se = o_ese in occ or o_sse in occ
        self.trim_nw = o_wnw in occ or o_nnw in occ
        self.trim_ne = o_ene in occ or o_nne in occ
        self.flip = (center.x + center.y + center.z) % 4 == 1

    # TODO: Make a render config that decouples the printer config details from the geometry
    def render(self, config, center=OctoVector()):
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

        if self.trim_ne:
            bottom_belt[0] -= (N + E) * trim / 2
            bottom_belt[3] -= (N + E) * trim / 2
        if self.trim_nw:
            top_belt[0] -= (N + W) * trim / 2
            top_belt[1] -= (N + W) * trim / 2
        if self.trim_sw:
            bottom_belt[1] -= (S + W) * trim / 2
            bottom_belt[2] -= (S + W) * trim / 2
        if self.trim_se:
            top_belt[2] -= (S + E) * trim / 2
            top_belt[3] -= (S + E) * trim / 2

        belts =np.array([top_belt, top_bottom_belt, bottom_top_belt, bottom_belt])

        if self.flip:
            belts = belts * np.array((1, 1, -1))
            belts = np.flip(belts, 1)

        mesh = belts_to_trimesh(belts)
        return mesh
        # mesh.apply_transform(trimesh.transformations.reflection_matrix())

        # faces = [seal_belt(top_belt),
        #          stitch_belts(top_belt, top_bottom_belt),
        #          stitch_belts(top_bottom_belt, bottom_top_belt),
        #          stitch_belts(bottom_top_belt, bottom_belt),
        #          seal_belt(bottom_belt, is_bottom=True)
        #          ]
        #
        # face_array = np.concatenate(faces)
        #
        # if (center.x + center.y + center.z) % 4 == 1:
        #     face_array = face_array * np.array((1, 1, -1))
        #     face_array = np.flip(face_array, 1)
        #
        # mesh = Mesh(np.zeros(face_array.shape[0], dtype=Mesh.dtype))
        # mesh.vectors = face_array
        # mesh.update_normals()
        #
        # mesh.translate(center.to_np() * config.cell_size / 4)
        #
        # return mesh


def single_cell_testing():
    tetra = TetraCell()

    config = OctoConfigs.config_25
    mesh1 = tetra.render(config, Vector3(1, 1, 1))
    mesh2 = tetra.render(config, Vector3(1, 1, -1))

    # octo1 = OctoCell().render()

    # RenderUtils.save_meshes(mesh1, mesh2)


if __name__ == "__main__":
    single_cell_testing()

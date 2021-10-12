import numpy as np
from euclid3 import *
from stl import mesh

from printing.octo.OctoCell import Trim, Crop, OctoCell
from printing.octo.OctoConfig import OctoConfig

EPS = 0.001

sqrt2 = math.sqrt(2)
sqrt22 = sqrt2 / 2

X2 = Vector3(2, 0, 0)
Y2 = Vector3(0, 2, 0)


class StlRenderer:

    def __init__(self):
        pass

    def render(self, config, *grids):
        assert config.overlap <= config.cell_size

        meshes = []

        for grid in grids:

            for center, cell in grid.occ.items():
                center = np.array(center) * (config.cell_size / 2, config.cell_size / 2, config.cell_size * sqrt22)
                meshes.append(
                    self.neo_trimmed_octo(cell, config.cell_size, config.overlap, config.slit, center))

        # for center, is_pyramid in grid.welding.items():
        #     center = np.array(center) * (cell_size / 2, cell_size / 2, cell_size * sqrt22)
        # meshes.append(self.welding_cube(overlap, slit, center, is_pyramid))

        return mesh.Mesh(np.concatenate([m.data for m in meshes]))

    def welding_cube(self, overlap, slit=0, center=(0, 0, 0), is_pyramid=False):
        size = (overlap + slit / 2)
        bottom_front_left = np.array([-1, -1, -1]) * size
        bottom_front_right = np.array([1, -1, -1]) * size
        bottom_back_right = np.array([1, 1, -1]) * size
        bottom_back_left = np.array([-1, 1, -1]) * size

        top_front_left = np.array([-1, -1, 1]) * size
        top_front_right = np.array([1, -1, 1]) * size
        top_back_right = np.array([1, 1, 1]) * size
        top_back_left = np.array([-1, 1, 1]) * size

        if is_pyramid:
            bottom_front_left[2] = 0
            bottom_front_right[2] = 0
            bottom_back_right[2] = 0
            bottom_back_left[2] = 0

        faces = np.array([

            [top_front_left, top_front_right, top_back_right],
            [top_back_right, top_back_left, top_front_left],

            [bottom_front_left, bottom_front_right, top_front_right],
            [top_front_right, top_front_left, bottom_front_left],

            [bottom_front_right, bottom_back_right, top_back_right],
            [top_back_right, top_front_right, bottom_front_right],

            [bottom_back_right, bottom_back_left, top_back_left],
            [top_back_left, top_back_right, bottom_back_right],

            [bottom_back_left, bottom_front_left, top_front_left],
            [top_front_left, top_back_left, bottom_back_left],

            [bottom_front_left, bottom_back_right, bottom_front_right],
            [bottom_back_right, bottom_front_left, bottom_back_left]

        ])

        cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        cube.vectors = faces
        cube.update_normals()
        cube.translate(center)

        return cube

    def stitch_belt_to_point(self, point, belt, bottom=False):

        faces = np.array([
            [belt[0], belt[1], point],
            [belt[1], belt[2], point],
            [belt[2], belt[3], point],
            [belt[3], belt[0], point],
        ])

        if bottom:
            faces = np.flip(faces, 1)

        return faces

    def stitch_belts(self, top_belt, bottom_belt):
        return np.array([
            [bottom_belt[0], bottom_belt[1], top_belt[0]],
            [bottom_belt[1], bottom_belt[2], top_belt[1]],
            [bottom_belt[2], bottom_belt[3], top_belt[2]],
            [bottom_belt[3], bottom_belt[0], top_belt[3]],

            [bottom_belt[1], top_belt[1], top_belt[0]],
            [bottom_belt[2], top_belt[2], top_belt[1]],
            [bottom_belt[3], top_belt[3], top_belt[2]],
            [bottom_belt[0], top_belt[0], top_belt[3]],
        ])

    def seal_belt(self, belt, bottom=False):
        faces = np.array([
            [belt[0], belt[1], belt[2]],
            [belt[0], belt[2], belt[3]],
        ])

        if bottom:
            faces = np.flip(faces, 1)

        return faces

    def neo_trimmed_octo(self,
                         cell,
                         size,
                         overlap,
                         slit,
                         center=(0, 0, 0),
                         ):

        oversize = size + overlap
        trim = overlap + slit / 2
        weld = overlap + slit / 2

        # print(size, overlap, oversize)

        top = np.array((0, 0, sqrt22)) * oversize
        bottom = np.array((0, 0, -sqrt22)) * oversize

        sw = np.array((-0.5, -0.5, 0))
        se = np.array((0.5, -0.5, 0))
        ne = np.array((0.5, 0.5, 0))
        nw = np.array((-0.5, 0.5, 0))
        up = np.array((0, 0, sqrt22))

        cropped_bottom = bottom + up * overlap

        cardinal = np.array((sw, se, ne, nw))

        equator_belt = cardinal * oversize

        equator_top_belt = equator_belt - cardinal * trim + up * trim
        equator_bottom_belt = equator_belt - cardinal * trim - up * trim

        top_solid_belt = np.copy(equator_belt) + up * oversize
        bottom_solid_belt = np.copy(equator_belt) - up * oversize

        top_belt = cardinal * overlap + top - up * overlap
        bottom_belt = cardinal * overlap + bottom + up * overlap

        up_welding_belt_top = cardinal * 2 * weld + top + 2 * up * weld
        up_welding_belt_bottom = np.copy(up_welding_belt_top) - 4 * up * weld

        down_welding_belt_top = cardinal * 2 * weld + bottom + 2 * up * weld
        down_welding_belt_bottom = cardinal * 2 * weld + bottom - up * 2 * weld

        faces = []

        if cell.is_solid:
            faces.append(self.seal_belt(top_solid_belt))
            faces.append(self.stitch_belts(top_solid_belt, bottom_solid_belt))
            faces.append(self.seal_belt(bottom_solid_belt, bottom=True))
        elif cell.is_pyramid:
            if cell.point_up:
                faces.append(self.stitch_belt_to_point(top, equator_belt))
                faces.append(self.seal_belt(equator_belt, bottom=True))
            else:
                faces.append(self.seal_belt(top_belt))
                faces.append(self.stitch_belts(top_belt, equator_belt))
                faces.append(self.seal_belt(equator_belt, bottom=True))
        else:  # Is a complete octo
            if Trim.FRONT in cell.trims:
                equator_belt[: 2, 1] = equator_top_belt[0, 1]
            if Trim.BACK in cell.trims:
                equator_belt[2:, 1] = equator_top_belt[2, 1]
            if Trim.RIGHT in cell.trims:
                equator_belt[1: 3, 0] = equator_top_belt[1, 0]
            if Trim.LEFT in cell.trims:
                equator_belt[3, 0] = equator_top_belt[0, 0]
                equator_belt[0, 0] = equator_top_belt[0, 0]

            # Top half
            if cell.weld_up:
                faces.append(self.seal_belt(up_welding_belt_top))
                faces.append(self.stitch_belts(up_welding_belt_top, up_welding_belt_bottom))
                faces.append(self.stitch_belts(up_welding_belt_bottom, equator_top_belt))
                faces.append(self.stitch_belts(equator_top_belt, equator_belt))
                faces.append(self.stitch_belts(equator_belt, equator_bottom_belt))
            elif cell.point_up:
                faces.append(self.stitch_belt_to_point(top, equator_top_belt))
                faces.append(self.stitch_belts(equator_top_belt, equator_belt))
                faces.append(self.stitch_belts(equator_belt, equator_bottom_belt))
            else:  # snipped top
                faces.append(self.seal_belt(top_belt))
                faces.append(self.stitch_belts(top_belt, equator_top_belt))
                faces.append(self.stitch_belts(equator_top_belt, equator_belt))
                faces.append(self.stitch_belts(equator_belt, equator_bottom_belt))

            # Bottom half
            if cell.weld_down:
                faces.append(self.stitch_belts(equator_bottom_belt, down_welding_belt_top))
                # faces.append(self.seal_belt(down_welding_belt_top))
                faces.append(self.stitch_belts(down_welding_belt_top, down_welding_belt_bottom))
                # faces.append(self.seal_belt(down_welding_belt_bottom, bottom=True))
                faces.append(self.stitch_belt_to_point(cropped_bottom, down_welding_belt_bottom, bottom=True))


            elif cell.point_down:
                faces.append(self.stitch_belt_to_point(bottom, equator_bottom_belt, bottom=True))
            else:  # Snipped bottom
                faces.append(self.stitch_belts(equator_bottom_belt, bottom_belt))
                faces.append(self.seal_belt(bottom_belt, bottom=True))


        if Crop.UP in cell.crops:
            pass


        # Make the faces into a mesh
        face_array = np.concatenate(faces)
        octo = mesh.Mesh(np.zeros(face_array.shape[0], dtype=mesh.Mesh.dtype))
        octo.vectors = face_array
        octo.update_normals()
        octo.translate(center)

        return octo


def testing():

    cell = OctoCell()
    config = OctoConfig()
    rendererer = StlRenderer()
    octo = rendererer.neo_trimmed_octo(cell, config.cell_size, config.overlap, config.slit)

    # print(octo.`)


if __name__=="__main__":
    testing()

        # Old bullshit delete when this is working

        # top_belt = top_cardinal * trim_top_bottom + top
        # equator_top_belt = top_cardinal * (size - trim) + top
        # equator_belt = top_cardinal * size + top
        #
        # equator_bottom_belt = bottom_cardinal * (size - trim) + bottom
        # bottom_belt = bottom_cardinal * trim_top_bottom + bottom
        #
        # top_welding_belt = bottom_cardinal * 2 * trim_top_bottom + bottom
        # bottom_welding_belt = np.copy(top_welding_belt)
        # bottom_welding_belt[:, 2] = bottom_belt[0, 2] + 0.1
        #
        # top_flange_belt = np.copy(equator_top_belt)
        # bottom_flange_belt = np.copy(equator_belt)
        #
        # if Trim.FRONT in trims:
        #     top_flange_belt[:2, 1] = bottom_flange_belt[0, 1]
        #     equator_belt[: 2, 1] = equator_top_belt[0, 1]
        # if Trim.BACK in trims:
        #     top_flange_belt[2:, 1] = bottom_flange_belt[2, 1]
        #     equator_belt[2:, 1] = equator_top_belt[2, 1]
        # if Trim.RIGHT in trims:
        #     top_flange_belt[1:3, 0] = bottom_flange_belt[1, 0]
        #     equator_belt[1: 3, 0] = equator_top_belt[1, 0]
        #
        # if Trim.LEFT in trims:
        #     top_flange_belt[3, 0] = bottom_flange_belt[0, 0]
        #     top_flange_belt[0, 0] = bottom_flange_belt[0, 0]
        #
        #     equator_belt[3, 0] = equator_top_belt[0, 0]
        #     equator_belt[0, 0] = equator_top_belt[0, 0]
        #
        # faces = []
        # faces.append(self.seal_belt(top_belt))
        # # faces.append(self.stitch_belt_to_point(top, top_belt))
        # faces.append(self.stitch_belts(top_belt, equator_top_belt))
        # faces.append(self.stitch_belts(equator_top_belt, equator_belt))
        #
        # if is_pyramid:
        #
        #     faces.append(self.seal_belt(top_flange_belt, top=True))
        #     faces.append(self.stitch_belts(top_flange_belt, bottom_flange_belt))
        #     faces.append(self.seal_belt(bottom_flange_belt, top=False))
        #
        #     # faces.append( self.seal_belt(equator_belt, top=False))
        # else:
        #
        #     # faces.append(self.stitch_belts(equator_belt, equator_bottom_belt))
        #     # faces.append(self.stitch_belts(equator_bottom_belt, bottom_belt))
        #     # faces.append(self.seal_belt(bottom_belt, top=False))
        #     pass
        #     # faces.append(self.stitch_belts(equator_bottom_belt, top_welding_belt))
        #     # faces.append(self.stitch_belts(top_welding_belt, bottom_welding_belt))
        #     # faces.append(self.seal_belt(bottom_welding_belt, top=False))

    # def trimmed_octo(self, size, overlap, slit, center=(0, 0, 0), trims=frozenset(), is_pyramid=False,
    #                  pyramid_floor=0.2):
    #
    #     size += overlap
    #     trim = overlap / 2 + slit / 2
    #     trim_bottom = overlap / 2
    #
    #     front_left = np.array((-0.5, -0.5, 0)) * size  # + (0, -trim.front, 0)
    #     front_right = np.array([0.5, -0.5, 0]) * size  # + (0, -trim.front, 0)
    #     back_right = np.array([0.5, 0.5, 0]) * size
    #     back_left = np.array([-0.5, 0.5, 0]) * size
    #     top = np.array([0, 0, sqrt22]) * size
    #     bottom = np.array([0, 0, -sqrt22]) * size
    #
    #     front_left_top = front_left + np.array((1, 1, sqrt2)) * trim
    #     front_right_top = front_right + np.array((-1, 1, sqrt2)) * trim
    #     back_right_top = back_right + np.array((-1, -1, sqrt2)) * trim
    #     back_left_top = back_left + np.array((1, -1, sqrt2)) * trim
    #
    #     front_left_bottom = front_left_top - np.array((0, 0, 2 * trim * sqrt2))
    #     front_right_bottom = front_right_top - np.array((0, 0, 2 * trim * sqrt2))
    #     back_right_bottom = back_right_top - np.array((0, 0, 2 * trim * sqrt2))
    #     back_left_bottom = back_left_top - np.array((0, 0, 2 * trim * sqrt2))
    #
    #     flange_bottom_front_left = np.array((-0.5, -0.5, 0)) * size  # + (0, -trim.front, 0)
    #     flange_bottom_front_right = np.array([0.5, -0.5, 0]) * size  # + (0, -trim.front, 0)
    #     flange_bottom_back_right = np.array([0.5, 0.5, 0]) * size
    #     flange_bottom_back_left = np.array([-0.5, 0.5, 0]) * size
    #
    #     flange_top_front_left = front_left + np.array((1, 1, sqrt2)) * pyramid_floor / sqrt2  # + (0, -trim.front, 0)
    #     flange_top_front_right = front_right + np.array((-1, 1, sqrt2)) * pyramid_floor / sqrt2  # + (0, -trim.front, 0)
    #     flange_top_back_right = back_right + np.array((-1, -1, sqrt2)) * pyramid_floor / sqrt2
    #     flange_top_back_left = back_left + np.array((1, -1, sqrt2)) * pyramid_floor / sqrt2
    #
    #     if is_pyramid and False:
    #         front_left_bottom = front_left + (0, 0, pyramid_floor)
    #         front_right_bottom = front_right + (0, 0, pyramid_floor)
    #         back_right_bottom = back_right + (0, 0, pyramid_floor)
    #         back_left_bottom = back_left + (0, 0, pyramid_floor)
    #
    #     bottom_front_left = bottom + np.array((-1, -1, sqrt2)) * trim_bottom
    #     bottom_front_right = bottom + np.array((1, -1, sqrt2)) * trim_bottom
    #     bottom_back_right = bottom + np.array((1, 1, sqrt2)) * trim_bottom
    #     bottom_back_left = bottom + np.array((-1, 1, sqrt2)) * trim_bottom
    #
    #     if is_pyramid and False:
    #         bottom_front_left = front_left.copy()
    #         bottom_front_right = front_right.copy()
    #         bottom_back_right = back_right.copy()
    #         bottom_back_left = back_left.copy()
    #
    #     if is_pyramid and False:
    #         front_left += (0, 0, pyramid_floor)
    #         front_right += (0, 0, pyramid_floor)
    #         back_left += (0, 0, pyramid_floor)
    #         back_right += (0, 0, pyramid_floor)
    #
    #     if Trim.FRONT in trims:
    #         front_left[1] += trim
    #         front_right[1] += trim
    #     if Trim.BACK in trims:
    #         back_left[1] -= trim
    #         back_right[1] -= trim
    #     if Trim.LEFT in trims:
    #         front_left[0] += trim
    #         back_left[0] += trim
    #     if Trim.RIGHT in trims:
    #         back_right[0] -= trim
    #         front_right[0] -= trim
    #
    #     # if is_pyramid:
    #     #     front_left[2] = pyramid_floor
    #     #     front_right[2] = pyramid_floor
    #     #     back_left[2] = pyramid_floor
    #     #     back_right[2] = pyramid_floor
    #
    #     # front_left_bottom[2] = pyramid_floor
    #     # front_right_bottom[2] = pyramid_floor
    #     # back_right_bottom[2] = pyramid_floor
    #     # back_left_bottom[2] = pyramid_floor
    #     #
    #     # bottom_front_left[2] = pyramid_floor
    #     # bottom_front_right[2] = pyramid_floor
    #     # bottom_back_right[2] = pyramid_floor
    #     # bottom_back_left[2] = pyramid_floor
    #
    #     # bottom += (0, 0, sqrt22 * trim.bottom)
    #
    #     faces = np.array([
    #         [front_left_top, front_right_top, top],
    #         [front_right_top, back_right_top, top],
    #         [back_right_top, back_left_top, top],
    #         [back_left_top, front_left_top, top],
    #
    #         [front_left_top, front_left, front_right_top],
    #         [front_right, front_right_top, front_left],
    #
    #         [front_right_top, front_right, back_right_top],
    #         [back_right, back_right_top, front_right],
    #
    #         [back_right_top, back_right, back_left_top],
    #         [back_left, back_left_top, back_right],
    #
    #         [back_left_top, back_left, front_left_top],
    #         [front_left, front_left_top, back_left]
    #     ]
    #
    #     )
    #
    #     if is_pyramid:
    #
    #         faces = np.append(faces, [
    #             [front_left, back_right, front_right],
    #             [back_right, front_left, back_left],
    #         ], axis=0)
    #
    #         if pyramid_floor > 0:
    #             faces = np.append(faces, [
    #                 [flange_top_front_left, flange_top_front_right, flange_top_back_right],
    #                 [flange_top_back_right, flange_top_back_left, flange_top_front_left],
    #                 [flange_bottom_back_right, flange_bottom_front_right, flange_bottom_front_left],
    #                 [flange_bottom_front_left, flange_bottom_back_left, flange_bottom_back_right],
    #
    #                 [flange_bottom_front_left, flange_bottom_front_right, flange_top_front_left],
    #                 [flange_top_front_right, flange_top_front_left, flange_bottom_front_right],
    #
    #                 [flange_bottom_front_right, flange_bottom_back_right, flange_top_front_right],
    #                 [flange_top_back_right, flange_top_front_right, flange_bottom_back_right],
    #
    #                 [flange_bottom_back_right, flange_bottom_back_left, flange_top_back_right],
    #                 [flange_top_back_left, flange_top_back_right, flange_bottom_back_left],
    #
    #                 [flange_bottom_back_left, flange_bottom_front_left, flange_top_back_left],
    #                 [flange_top_front_left, flange_top_back_left, flange_bottom_front_left]
    #
    #             ], axis=0)
    #
    #     else:
    #
    #         faces = np.append(faces, [
    #
    #             [front_left, front_left_bottom, front_right],
    #             [front_right_bottom, front_right, front_left_bottom],
    #
    #             [front_right, front_right_bottom, back_right],
    #             [back_right_bottom, back_right, front_right_bottom],
    #
    #             [back_right, back_right_bottom, back_left],
    #             [back_left_bottom, back_left, back_right_bottom],
    #
    #             [back_left, back_left_bottom, front_left],
    #             [front_left_bottom, front_left, back_left_bottom],
    #
    #             [front_right_bottom, front_left_bottom, bottom_front_left],
    #             [back_right_bottom, front_right_bottom, bottom_front_right],
    #             [back_left_bottom, back_right_bottom, bottom_back_right],
    #             [front_left_bottom, back_left_bottom, bottom_back_left],
    #
    #             [bottom_front_left, bottom_front_right, front_right_bottom],
    #             [bottom_front_right, bottom_back_right, back_right_bottom],
    #             [bottom_back_right, bottom_back_left, back_left_bottom],
    #             [bottom_back_left, bottom_front_left, front_left_bottom],
    #
    #             [bottom_front_left, bottom_back_left, bottom_back_right],
    #             [bottom_back_right, bottom_front_right, bottom_front_left]
    #
    #         ], axis=0)
    #
    #     octo = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    #     octo.vectors = faces
    #     octo.update_normals()
    #     octo.translate(center)
    #
    #     return octo

# nozzle = 0.6
# nozzle_width_multiplier = 2
# layer_height_multipler = 2
# overlap_ratio = 0.1
# line_width = round(nozzle * nozzle_width_multiplier, 3)
# line_layer_ratio = 2
# layer_height = round(line_width/line_layer_ratio, 3)
# first_layer_multiplier = 1
# overlap_ratio = .1
# target_overlap_cell_ratio = 3


# 0.4 mm nozzle
# line_width = 0.4
# layer_height = round(line_width/4, 2)
# first_layer_multiplier = 1.5
# overlap_ratio = 1
# target_overlap_cell_ratio = 1

# 0.3 mm nozzle
# nozzle = 0.3
# nozzle_width_multiplier = 1 + 1/3
# line_layer_ratio = 2
# overlap_ratio = 0.1
# line_width = round(nozzle * nozzle_width_multiplier, 3)
# layer_height = round(line_width/line_layer_ratio, 3)
# first_layer_multiplier = 1.5
# target_overlap_cell_ratio = 4
#
# for line_layer_ratio in (1.1, 1.25, 1.5, 2, 2.5):
#     print(round(line_width/line_layer_ratio, 3))
#
#
# slit = line_width/1000
# overlap = slit + line_width + (1-overlap_ratio) *  line_width * (sqrt2 -1 ) + 0.0001
#
# target_cell_size = 1 *  target_overlap_cell_ratio * overlap
# target_layers = math.ceil(target_cell_size * sqrt22 /layer_height)
# layers = target_layers
#
# # layers = 3
#
# cell_size = layers * layer_height / sqrt22
# pyramid_floor = overlap/2
# solid_layers = round(1 + (pyramid_floor - first_layer_multiplier * layer_height)/layer_height)
#
# print(overlap, target_cell_size, target_layers, layers)
#
#
#
# print("Settings")
# print("Line width:", line_width)
# print("Layer height:", layer_height)
#
# print("Solid Layers:", solid_layers)
# print()
# print("Other stats")
# print("Layers per cell:", layers)
# print("First layer height:", first_layer_multiplier * layer_height)
# print("Floor thickness:", pyramid_floor)
# print("Cell Size:", cell_size)
# print("Overlap:", overlap)
# print("size/overlap:", cell_size/overlap)


# gen = OctoConfigGenerator()
# config = gen.generate()
#
#
#
# grid = OctoGrid()
#
# iteration = 4
#
# tower(grid, iteration)
# # grid.make_flake(iteration)
# # grid.make_flake(iteration-1, center = (0, 0, 2 ** (iteration)))
#
# # grid.stellate(iteration-1, offset=2 ** iteration)
#
#
# grid.compute_trimming()
# grid.crop(z_min=2 ** (iteration-1))
#
#
# grid.compute_trimming()
#
# print(len(grid.occ.items()))
#
# renderer = StlRenderer()
# flake = renderer.render_with_config(grid, config)
#
# # flake = renderer.render(grid, cell_size, overlap, slit,pyramid_floor= 0)
#
# flake.save(TEST_FILE_NAME, mode=Mode.BINARY)
#

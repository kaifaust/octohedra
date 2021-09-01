import math

from GridBased import OctoGrid, Trim
from enum import Enum
import numpy as np
import stl
from stl import mesh
from stl import Mode


TEST_FILE_NAME = "/Users/silver/Desktop/derp.stl"


from euclid3 import *

sqrt2 = math.sqrt(2)
sqrt22 = sqrt2 / 2

X2 = Vector3(2, 0, 0)
Y2 = Vector3(0, 2, 0)










class StlRenderer:


    def __init__(self):
        pass

    def render(self, grid, cell_size, overlap, slit, pyramid_floor = 0.3):
        meshes = []
        for center, cell in grid.occ.items():

            center = np.array(center) * (cell_size /2, cell_size /2, cell_size *sqrt22)
            meshes.append(self.trimmed_octo(cell_size, overlap, slit, center, cell.trims, cell.is_pyramid, pyramid_floor))

        for center, is_pyramid in grid.welding.items():
            center = np.array(center) * (cell_size / 2, cell_size / 2, cell_size * sqrt22)
            meshes.append(self.welding_cube(overlap, slit, center, is_pyramid))

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

    def trimmed_octo(self, size, overlap, slit, center=(0, 0, 0), trims=frozenset(), is_pyramid=False, pyramid_floor= 0.2):


        size += overlap
        trim = overlap / 2 + slit / 2
        trim_bottom = overlap / 2

        front_left = np.array((-0.5, -0.5, 0)) * size  # + (0, -trim.front, 0)
        front_right = np.array([0.5, -0.5, 0]) * size  # + (0, -trim.front, 0)
        back_right = np.array([0.5, 0.5, 0]) * size
        back_left = np.array([-0.5, 0.5, 0]) * size
        top = np.array([0, 0, sqrt22]) * size
        bottom = np.array([0, 0, -sqrt22]) * size

        front_left_top = front_left + np.array((1, 1, sqrt2)) * trim
        front_right_top = front_right + np.array((-1, 1, sqrt2)) * trim
        back_right_top = back_right + np.array((-1, -1, sqrt2)) * trim
        back_left_top = back_left + np.array((1, -1, sqrt2)) * trim

        front_left_bottom = front_left_top - np.array((0, 0, 2 * trim * sqrt2))
        front_right_bottom = front_right_top - np.array((0, 0, 2 * trim * sqrt2))
        back_right_bottom = back_right_top - np.array((0, 0, 2 * trim * sqrt2))
        back_left_bottom = back_left_top - np.array((0, 0, 2 * trim * sqrt2))

        flange_bottom_front_left = np.array((-0.5, -0.5, 0)) * size  # + (0, -trim.front, 0)
        flange_bottom_front_right = np.array([0.5, -0.5, 0]) * size  # + (0, -trim.front, 0)
        flange_bottom_back_right = np.array([0.5, 0.5, 0]) * size
        flange_bottom_back_left = np.array([-0.5, 0.5, 0]) * size


        flange_top_front_left = front_left + np.array((1, 1, sqrt2)) * pyramid_floor/sqrt2  # + (0, -trim.front, 0)
        flange_top_front_right = front_right + np.array((-1, 1, sqrt2)) * pyramid_floor/sqrt2  # + (0, -trim.front, 0)
        flange_top_back_right = back_right + np.array((-1, -1, sqrt2)) * pyramid_floor/sqrt2
        flange_top_back_left = back_left + np.array((1, -1, sqrt2)) * pyramid_floor/sqrt2

        if is_pyramid and False:
            front_left_bottom = front_left + (0, 0, pyramid_floor)
            front_right_bottom = front_right+ (0, 0, pyramid_floor)
            back_right_bottom = back_right+ (0, 0, pyramid_floor)
            back_left_bottom = back_left+ (0, 0, pyramid_floor)



        bottom_front_left = bottom + np.array((-1, -1, sqrt2)) * trim_bottom
        bottom_front_right = bottom + np.array((1, -1, sqrt2)) * trim_bottom
        bottom_back_right = bottom + np.array((1, 1, sqrt2)) * trim_bottom
        bottom_back_left = bottom + np.array((-1, 1, sqrt2)) * trim_bottom

        if is_pyramid and False:
            bottom_front_left = front_left.copy()
            bottom_front_right = front_right.copy()
            bottom_back_right = back_right.copy()
            bottom_back_left = back_left.copy()

        if is_pyramid and False:
            front_left += (0, 0, pyramid_floor)
            front_right += (0, 0, pyramid_floor)
            back_left += (0, 0, pyramid_floor)
            back_right += (0, 0, pyramid_floor)



        if Trim.FRONT in trims:
            front_left[1] += trim
            front_right[1] += trim
        if Trim.BACK in trims:
            back_left[1] -= trim
            back_right[1] -= trim
        if Trim.LEFT in trims:
            front_left[0] += trim
            back_left[0] += trim
        if Trim.RIGHT in trims:
            back_right[0] -= trim
            front_right[0] -= trim

        # if is_pyramid:
        #     front_left[2] = pyramid_floor
        #     front_right[2] = pyramid_floor
        #     back_left[2] = pyramid_floor
        #     back_right[2] = pyramid_floor

            # front_left_bottom[2] = pyramid_floor
            # front_right_bottom[2] = pyramid_floor
            # back_right_bottom[2] = pyramid_floor
            # back_left_bottom[2] = pyramid_floor
            #
            # bottom_front_left[2] = pyramid_floor
            # bottom_front_right[2] = pyramid_floor
            # bottom_back_right[2] = pyramid_floor
            # bottom_back_left[2] = pyramid_floor

        # bottom += (0, 0, sqrt22 * trim.bottom)

        faces = np.array([
            [front_left_top, front_right_top, top],
            [front_right_top, back_right_top, top],
            [back_right_top, back_left_top, top],
            [back_left_top, front_left_top, top],

            [front_left_top, front_left, front_right_top],
            [front_right, front_right_top, front_left],

            [front_right_top, front_right, back_right_top],
            [back_right, back_right_top, front_right],

            [back_right_top, back_right, back_left_top],
            [back_left, back_left_top, back_right],

            [back_left_top, back_left, front_left_top],
            [front_left, front_left_top, back_left]
        ]

        )

        if is_pyramid:

            faces = np.append(faces, [
                [front_left, back_right, front_right],
                [back_right, front_left, back_left],
            ], axis=0)

            if pyramid_floor >0:
                faces = np.append(faces, [
                    [flange_top_front_left, flange_top_front_right, flange_top_back_right],
                    [flange_top_back_right, flange_top_back_left, flange_top_front_left],
                    [flange_bottom_back_right, flange_bottom_front_right, flange_bottom_front_left],
                    [flange_bottom_front_left, flange_bottom_back_left, flange_bottom_back_right],




                    [flange_bottom_front_left, flange_bottom_front_right, flange_top_front_left],
                    [flange_top_front_right, flange_top_front_left, flange_bottom_front_right],

                    [flange_bottom_front_right, flange_bottom_back_right, flange_top_front_right],
                    [flange_top_back_right, flange_top_front_right, flange_bottom_back_right],

                    [flange_bottom_back_right, flange_bottom_back_left, flange_top_back_right],
                    [flange_top_back_left, flange_top_back_right, flange_bottom_back_left],

                    [flange_bottom_back_left, flange_bottom_front_left, flange_top_back_left],
                    [flange_top_front_left, flange_top_back_left, flange_bottom_front_left]


                ], axis=0)

        else:






            faces = np.append(faces, [

                [front_left, front_left_bottom, front_right],
                [front_right_bottom, front_right, front_left_bottom],

                [front_right, front_right_bottom, back_right],
                [back_right_bottom, back_right, front_right_bottom],

                [back_right, back_right_bottom, back_left],
                [back_left_bottom, back_left, back_right_bottom],

                [back_left, back_left_bottom, front_left],
                [front_left_bottom, front_left, back_left_bottom],

                [front_right_bottom, front_left_bottom, bottom_front_left],
                [back_right_bottom, front_right_bottom, bottom_front_right],
                [back_left_bottom, back_right_bottom, bottom_back_right],
                [front_left_bottom, back_left_bottom, bottom_back_left],

                [bottom_front_left, bottom_front_right, front_right_bottom],
                [bottom_front_right, bottom_back_right, back_right_bottom],
                [bottom_back_right, bottom_back_left, back_left_bottom],
                [bottom_back_left, bottom_front_left, front_left_bottom],

                [bottom_front_left, bottom_back_left, bottom_back_right],
                [bottom_back_right, bottom_front_right, bottom_front_left]

            ], axis=0)

        octo = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        octo.vectors = faces
        octo.update_normals()
        octo.translate(center)

        return octo






def tower(grid, iteration, center=(0, 0, 0), evil=frozenset(), full_evil = False):

    z = 0
    center = np.array(center)
    for i in range(iteration, 0, -1):
        grid.make_flake(i, (center[0], center[1], center[2] + z))

        if i in evil or (full_evil and iteration >= i > 1):

            exy = evil_offset_xy = 2 ** (i) - 2 ** (i-2)
            ez = evil_offset_z = z + 2 ** (i-2)
            tower(grid, i-1, center + (exy, exy, ez))
            tower(grid, i-1, center + (exy, -exy, ez))
            tower(grid, i-1, center + (-exy, exy, ez))
            tower(grid, i-1, center + (-exy, -exy, ez))

            # grid.make_flake(i-1, center +  (exy, exy, ez))
            # grid.make_flake(i-1, center +  (exy, -exy, ez))
            # grid.make_flake(i-1, center +  (-exy, exy, ez))
            # grid.make_flake(i-1, center + (-exy, -exy, ez))


        z += 2 ** i


def tower_complex(grid, iteration, center=(0, 0, 0)):
    if iteration < 1:
        return
    tower(grid, iteration, center, full_evil=True)
    tower_complex(grid, iteration - 1, (center[0] + 2 ** iteration, center[1] + 2 ** iteration, center[2]))
    tower_complex(grid, iteration - 1, (center[0] + 2 ** iteration, center[1] - 2 ** iteration, center[2]))
    tower_complex(grid, iteration - 1, (center[0] - 2 ** iteration, center[1] + 2 ** iteration, center[2]))
    tower_complex(grid, iteration - 1, (center[0] - 2 ** iteration, center[1] - 2 ** iteration, center[2]))


iteration = 3







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
nozzle = 0.3
nozzle_width_multiplier = 1 + 1/3
line_layer_ratio = 2
overlap_ratio = 0.1
line_width = round(nozzle * nozzle_width_multiplier, 3)
layer_height = round(line_width/line_layer_ratio, 3)
first_layer_multiplier = 1.5
target_overlap_cell_ratio = 4

for line_layer_ratio in (1.1, 1.25, 1.5, 2, 2.5):
    print(round(line_width/line_layer_ratio, 3))


slit = line_width/1000
overlap = slit + line_width + (1-overlap_ratio) *  line_width * (sqrt2 -1 ) + 0.0001

target_cell_size = 1 *  target_overlap_cell_ratio * overlap
target_layers = math.ceil(target_cell_size * sqrt22 /layer_height)
layers = target_layers

# layers = 3

cell_size = layers * layer_height / sqrt22
pyramid_floor = overlap/2
solid_layers = round(1 + (pyramid_floor - first_layer_multiplier * layer_height)/layer_height)

print(overlap, target_cell_size, target_layers, layers)



print("Settings")
print("Line width:", line_width)
print("Layer height:", layer_height)

print("Solid Layers:", solid_layers)
print()
print("Other stats")
print("Layers per cell:", layers)
print("First layer height:", first_layer_multiplier * layer_height)
print("Floor thickness:", pyramid_floor)
print("Cell Size:", cell_size)
print("Overlap:", overlap)
print("size/overlap:", cell_size/overlap)


grid = OctoGrid()


tower(grid, iteration)
# grid.make_flake(iteration)
# grid.make_flake(iteration-1, center = (0, 0, 2 ** (iteration)))

# grid.stellate(iteration-1, offset=2 ** iteration)


grid.compute_trimming()
grid.crop(z_min=2 ** (iteration-1))


grid.compute_trimming()

print(len(grid.occ.items()))

renderer = StlRenderer()

flake = renderer.render(grid, cell_size, overlap, slit,pyramid_floor= 0)

flake.save(TEST_FILE_NAME)#, mode=Mode.ASCII)


exit()

# grid.make_flake(iteration,(0, -0,  10))
# grid.six_way()

# tower(grid, 4, evil=[4, 2, 3])
# grid.make_flake(2, (2 ** 3 - 2 ** 1, 2 ** 3 - 2 ** 1, 2 ** 4 + 2 ** 1))
# grid.make_flake(2, (-2 ** 3 - 2 ** 1, 2 ** 3 - 2 ** 1, 2 ** 4 + 2 ** 1))
# grid.make_flake(2, (2 ** 3 - 2 ** 1, -2 ** 3 - 2 ** 1, 2 ** 4 + 2 ** 1))
# grid.make_flake(2, (-2 ** 3 - 2 ** 1, -2 ** 3 - 2 ** 1, 2 ** 4 + 2 ** 1))


###################################### 4 tower comples


# tower(grid, 3)
# tower(grid, 4, (2 ** 3, 2 ** 3, 0))













# grid.make_flake(iteration)
# print(list(filter(lambda key: key[2] == 1, grid.occ.keys())))
# grid.clear(iteration)
# print(grid.occ.keys())
# grid.faces(iteration, ending_iteration=0, tetra_left=True, tetra_right=True)
# grid.faces(iteration-1, center=(2 ** iteration, 0, 2 ** iteration / 2), tetra_left=True)
# grid.faces(iteration-1, center=(-2 ** iteration, 0, 2 ** iteration / 2), tetra=True)


# grid.make_flake(iteration - 1, center=(2 ** iteration, 0, 2 ** iteration / 2))
# grid.make_flake(iteration - 1, center=(-2 ** iteration, 0, 2 ** iteration / 2))
# grid.make_flake(iteration - 1, center=(0, 2 ** iteration, 2 ** iteration / 2))
# grid.make_flake(iteration - 1, center=(0, -2 ** iteration, 2 ** iteration / 2))
#
# grid.make_flake(iteration - 2, center=(2 ** iteration / 2, 0, 2 ** iteration * 3 / 4))
# grid.make_flake(iteration - 2, center=(-2 ** iteration / 2, 0, 2 ** iteration * 3 / 4))
# grid.make_flake(iteration - 2, center=(0, 2 ** iteration / 2, 2 ** iteration * 3 / 4))
# grid.make_flake(iteration - 2, center=(0, -2 ** iteration / 2, 2 ** iteration * 3 / 4))

# grid.stellate(iteration-1, offset=2 ** iteration)
# grid.stellate(iteration-2, offset=2 ** iteration + 2 ** (iteration-1))
# grid.stellate(iteration-3, offset=2 ** iteration + 2 ** (iteration-1) + 2 ** (iteration-2))



# tower_complex(grid, iteration)
grid.compute_trimming()
grid.crop(z_min=0)

grid.compute_trimming()

print(len(grid.occ.items()))

renderer = StlRenderer()

# cell_size = 1
# overlap = .25 * sqrt22 * sqrt22 + .001
# slit = .00001


flake = renderer.render(grid, cell_size, overlap, slit,pyramid_floor= 1.5 * layer_height)
# flake = renderer.trimmed_octo(10, 1, .1, trims= {Trim.FRONT, Trim.RIGHT}, is_pyramid=True)
# flake = renderer.welding_cube(1, .1, is_pyramid=False)


# print(grid.occ)
# print(flake.data)
flake.save(TEST_FILE_NAME)#, mode=Mode.ASCII)

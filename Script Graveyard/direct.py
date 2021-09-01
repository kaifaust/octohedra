import math
import stl
from stl import mesh
import numpy as np
from collections import namedtuple
from timeit import default_timer as timer
from enum import Enum

# Create 3 faces of a cube
data = np.zeros(6, dtype=mesh.Mesh.dtype)

# Top of the cube
# x, z, y
sqrt2 = math.sqrt(2)
sqrt22 = math.sqrt(2) / 2


TEST_FILE_NAME = "/Users/silver/Desktop/derp.stl"


def octo(size=1, overlap=0, translation=(0, 0, 0), is_pyramid=False):
    vertices = np.array([
        [-0.5, -0.5, 0],  # belt
        [0.5, -0.5, 0],
        [0.5, 0.5, 0],
        [-0.5, 0.5, 0],
        [0, 0, sqrt22],  # top
        [0, 0, -sqrt22],  # bottom
    ])

    octo_faces = np.array([
        [0, 1, 4],  # top pyramid
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [1, 0, 5],  # bottom pyramid
        [2, 1, 5],
        [3, 2, 5],
        [0, 3, 5],
    ])

    pyramid_faces = np.array([
        [0, 1, 4],  # top pyramid
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 2, 1],
        [2, 0, 3]

    ])

    faces = pyramid_faces if is_pyramid else octo_faces

    return mesh_from_vertices(vertices, faces, size + overlap, translation)


def mesh_from_vertices(vertices, faces, scale=1, translation=(0, 0, 0), rotation_deg=0, rotation_axis=(0, 0, 1)):
    m = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = vertices[f[j], :] * scale

    m.update_normals()
    m.rotate(rotation_axis, math.radians(rotation_deg))
    m.translate(np.array(translation))
    # cube.vectors *= size + overlap

    return m


Trimming = namedtuple("Trimming", ["front", "bottom"])

class Trim(Enum):
    ALL = 1
    NONE = 2
    THREE = 3
    TWO = 4
    KERN = 5


def trimmed_octo(size, overlap, slit, center = (0, 0, 0), trim_type = Trim.ALL, is_pyramid = False):

    size += overlap
    trim = overlap/2 + slit/2
    trim_bottom = overlap/2

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



    front_left_bottom = front_left_top - np.array((0, 0,2 * trim * sqrt2))
    front_right_bottom = front_right_top - np.array((0, 0, 2 * trim * sqrt2))
    back_right_bottom = back_right_top - np.array((0, 0, 2 * trim * sqrt2))
    back_left_bottom = back_left_top - np.array((0, 0, 2* trim * sqrt2))



    bottom_front_left = bottom + np.array((-1, -1, sqrt2)) * trim_bottom
    bottom_front_right = bottom + np.array((1, -1, sqrt2)) * trim_bottom
    bottom_back_right = bottom + np.array((1, 1, sqrt2)) * trim_bottom
    bottom_back_left = bottom + np.array((-1, 1, sqrt2)) * trim_bottom

    if trim_type in {Trim.ALL, Trim.TWO, Trim.THREE}:
        front_left += (0, trim, 0)
        front_right += (-trim, trim, 0)
        back_right += (-trim, 0, 0)
    if trim_type in {Trim.ALL, Trim.THREE}:
        back_right += (0, -trim, 0)
        back_left += (0, -trim, 0)
    if trim_type is Trim.ALL:
        back_left += (trim, 0, 0)
        front_left += (trim, 0, 0)



    if is_pyramid:
        front_left_bottom[2] = 0
        front_right_bottom[2] = 0
        back_right_bottom[2] = 0
        back_left_bottom[2] = 0

        bottom_front_left[2] = 0
        bottom_front_right[2] = 0
        bottom_back_right[2] = 0
        bottom_back_left[2] = 0




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
        [front_left, front_left_top, back_left],

        [front_left, front_left_bottom, front_right],
        [front_right_bottom, front_right, front_left_bottom],

        [front_right, front_right_bottom, back_right],
        [back_right_bottom, back_right, front_right_bottom],

        [back_right, back_right_bottom, back_left],
        [back_left_bottom, back_left, back_right_bottom],

        [back_left, back_left_bottom, front_left],
        [front_left_bottom, front_left, back_left_bottom],



        # [front_left, front_right, top],
        # [front_right, back_right, top],
        # [back_right, back_left, top],
        # [back_left, front_left, top],

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

    ])

    # print(faces)

    octo = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    octo.vectors = faces
    octo.update_normals()
    octo.translate(center)


    return octo

def join_meshes(meshes):
    return mesh.Mesh(np.concatenate([m.data for m in meshes]))

# trim = Trimming(front=.1, bottom=.1)
#

size = 10

overlap = 2
slit = 1


octos = []

for i,pyramid in enumerate([True, False]):
    for j,trim in enumerate(Trim):
        octos.append(trimmed_octo(size, overlap, slit, center=(size * 1.5 * i, size * 1.5 * j, 0) ,trim_type=trim, is_pyramid=pyramid))

#
# o1 = octo(10)
# print(o1.data)
# print(o2.data)
# o2.save(TEST_FILE_NAME)
#
# exit()



octomesh = join_meshes(octos)
octomesh.save(TEST_FILE_NAME)

exit()



def octo_flake(iteration, size, overlap, slit, center, is_pyramid=True):
    if iteration == 0:
        return trimmed_octo(size, overlap, slit, center, is_pyramid)
    else:

        c = np.array(center)

        octos = []
        octos.append(octo_flake(iteration - 1, size / 2, overlap, slit, c + (size / 4, size / 4, 0), is_pyramid))
        octos.append(octo_flake(iteration - 1, size / 2, overlap,slit, c + (size / 4, -size / 4, 0), is_pyramid))
        octos.append(octo_flake(iteration - 1, size / 2, overlap,slit, c + (-size / 4, size / 4, 0), is_pyramid))
        octos.append(octo_flake(iteration - 1, size / 2, overlap,slit, c + (-size / 4, -size / 4, 0), is_pyramid))

        octos.append(octo_flake(iteration - 1, size / 2, overlap,slit, c + (0, 0, sqrt22 * size / 2), False))
        if not is_pyramid:
            octos.append(octo_flake(iteration - 1, size / 2, overlap,slit, c + (0, 0, -sqrt22 * size / 2), False))
        return join_meshes(octos)
        # octos.append(octo(size=size/2, overlap=overlap, translation=(1/2, 0, sqrt22)))
        # octos.append(octo(size=size/2, overlap=overlap, translation=(1/2, 1/2, -sqrt22)))


# octos = [octo(size=size, overlap=overlap, translation=(0, 0, 0))]
# octos.append(octo(size=size, overlap=overlap, translation=(1, 0, 0)))
# octos.append(octo(size=size, overlap=overlap, translation=(1, 1, 0)))
# octos.append(octo(size=size, overlap=overlap, translation=(0, 1, 0)))
# octos.append(octo(size=size, overlap=overlap, translation=(1/2, 1/2, sqrt22)))
# octos.append(octo(size=size, overlap=overlap, translation=(1/2, 1/2, -sqrt22)))
# octo2 = octo((1, 0, 0))
# octo3 = octo((1, 1, 0))
# octo4 = octo((0, 1, 0))
# octo5 = octo((1/2, 1/2, sqrt22))
# octo6 = octo((1/2, 1/2, -sqrt22))


# cube = join_meshes(octos)
iteration = 5
spacing = 5
size = spacing * 2 ** iteration
overlap = 1
slit = 0.1

start = timer()
cube = octo_flake(iteration, size, overlap, slit, (0, 0, 0))
end_generation = timer()
# print(cube.data)


# center = np.array((1, 2, 3))
#
# print(center)
#
# print(center * 2)
#
# print(center + (3, 4, 5))

cube.save("/Users/silver/Desktop/derp.stl")
end_export = timer()
print(f"Time to generate {end_generation-start:.4f}, time to export {end_export- end_generation:.4f}")
exit()

# data['vectors'][1] = numpy.array([[1, 0, 1],
#                                   [0, 1, 1],
#                                   [1, 1, 1]])
# # Front face
# data['vectors'][2] = numpy.array([[1, 0, 0],
#                                   [1, 0, 1],
#                                   [1, 1, 0]])
# data['vectors'][3] = numpy.array([[1, 1, 1],
#                                   [1, 0, 1],
#                                   [1, 1, 0]])
# # Left face
# data['vectors'][4] = numpy.array([[0, 0, 0],
#                                   [1, 0, 0],
#                                   [1, 0, 1]])
# data['vectors'][5] = numpy.array([[0, 0, 0],
#                                   [0, 0, 1],
#                                   [1, 0, 1]])


# Since the cube faces are from 0 to 1 we can move it to the middle by
# substracting .5
# data['vectors'] -= .5


# Generate 4 different meshes so we can rotate them later
meshes = [mesh.Mesh(data.copy()) for _ in range(4)]

# Rotate 90 degrees over the Y axis
meshes[0].rotate([0.0, 0.5, 0.0], math.radians(90))

# Translate 2 points over the X axis
meshes[1].x += 2

# Rotate 90 degrees over the X axis
meshes[2].rotate([0.5, 0.0, 0.0], math.radians(90))
# Translate 2 points over the X and Y points
meshes[2].x += 2
meshes[2].y += 2

# Rotate 90 degrees over the X and Y axis
meshes[3].rotate([0.5, 0.0, 0.0], math.radians(90))
meshes[3].rotate([0.0, 0.5, 0.0], math.radians(90))
# Translate 2 points over the Y axis
meshes[3].y += 2

meshes.pop().save("derp.stl")

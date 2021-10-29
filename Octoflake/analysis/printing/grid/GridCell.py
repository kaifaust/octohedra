import math

import numpy as np
from trimesh import Trimesh, geometry, transformations, util

from printing.grid.OctoVector import OctoVector
from printing.utils.OctoConfig import OctoConfig


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


def seal_belt(belt, is_bottom=False):
    faces = np.array([
        [belt[0], belt[1], belt[2]],
        [belt[0], belt[2], belt[3]],
        ])

    if is_bottom:
        faces = np.flip(faces, 1)

    return faces


def belts_to_trimesh(belts):
    point_dict = dict()
    points = []
    faces = []
    i = 0


    for point in belts.reshape((-1, 3)):
        t_point = tuple(point)
        if t_point not in point_dict:
            point_dict[t_point] = i
            points.append(t_point)
            i += 1

    def lookup(p):
        return point_dict[tuple(p)]

    faces.append([lookup(point) for point in belts[0]])
    faces.append([lookup(point) for point in reversed(belts[-1])])
    # faces.append([point_dict[tuple(point)] for point in reversed(belts[-1])])


    for j in range(len(belts) - 1):
        top_belt = belts[j]
        bottom_belt = belts[j + 1]

        for k in range(len(bottom_belt)):
            faces.append((
                lookup(bottom_belt[k - 1]),
                lookup(bottom_belt[k]),
                lookup(top_belt[k]),
                lookup(top_belt[k - 1])
                ))

    # geometry.vertex_face_indices()

    # top = belts[0]
    # bottom = belts[-1]
    #
    # faces.append([lookup(top[0]), lookup(top[1]), lookup(top[2])])
    # faces.append([lookup(top[0]), lookup(top[2]), lookup(top[3])])
    #
    # faces.append([lookup(bottom[0]), lookup(bottom[2]), lookup(bottom[1])])
    # faces.append([lookup(bottom[0]), lookup(bottom[3]), lookup(bottom[2])])
    #
    # # faces.append([point_dict[tuple(point)] for point in belts[0]])
    # # faces.append([point_dict[tuple(point)] for point in reversed(belts[-1])])
    #

    #
    #     top_belt = belts[j]
    #     bottom_belt = belts[j + 1]
    #     for i in range(len(top_belt)):
    #         faces.append([
    #             lookup(bottom_belt[i - 1]),
    #             lookup(bottom_belt[i]),
    #             lookup(top_belt[i - 1])])
    #         faces.append([
    #             lookup(bottom_belt[i]),
    #             lookup(top_belt[i]),
    #             lookup(top_belt[i - 1])])
    #         faces.append([
    #             lookup(bottom_belt[i]),
    #             lookup(top_belt[i]),
    #             lookup(top_belt[i - 1])])





    mesh = Trimesh(points, faces , validate=True)
    # mesh.remove_unreferenced_vertices()
    # mesh.remove_degenerate_faces()
    # mesh.remove_duplicate_faces()




    return mesh

    exit()

    points = list(set(map(tuple, old_mesh.vectors.reshape((-1, 3)))))

    point_dict = {point: i for i, point in enumerate(points)}

    faces = []
    for p1, p2, p3 in old_mesh.vectors:
        faces.append(
                (point_dict[tuple(p1)],
                 point_dict[tuple(p2)],
                 point_dict[tuple(p3)]
                 ))


class GridCell:

    def __init__(self):
        self.crops = set()
        self.trims = set()

    def trim(self, grid):
        pass

    def render(self, config: OctoConfig, center: OctoVector):
        raise NotImplementedError()

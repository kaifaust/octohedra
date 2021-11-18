from dataclasses import dataclass
from typing import Set

import numpy as np
from trimesh import Trimesh

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

    mesh = Trimesh(points, faces, validate=True)
    mesh.remove_unreferenced_vertices()
    mesh.remove_degenerate_faces()
    mesh.remove_duplicate_faces()

    return mesh

@dataclass
class GridCell:

    def trim(self, center: OctoVector, occ=Set[OctoVector]):
        raise NotImplementedError()

    def render(self, config: OctoConfig, center: OctoVector):
        raise NotImplementedError()

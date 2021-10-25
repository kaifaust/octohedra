import numpy as np

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


class GridCell:

    def __init__(self):
        self.crops = set()
        self.trims = set()






    def render(self, center, config: OctoConfig):
        raise NotImplementedError()

# def testing():
#     top_belt = [1, 2, 3]
#     bottom_belt = ["a", "b", "c"]
#     print(stitch_belts(top_belt, bottom_belt))

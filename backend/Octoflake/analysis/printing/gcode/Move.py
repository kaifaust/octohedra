import math
from dataclasses import dataclass, field
from typing import List

from printing.grid.OctoVector import OctoVector


def flow_rate(layer_height, line_width, filament_diameter=1.75):
    filament_area = 1 / 2 * math.pi * (filament_diameter / 2) ** 2
    line_area = layer_height * line_width  # - math.pi * (layer_height / 2) ** 2

    return line_area / filament_area


@dataclass
class MoveConfig:

    in_plane: bool = True
    is_extruding: bool = True

    # How fast the print head should try to move
    feed_rate: float = 20  # mm/s
    starting_feed_rate: float = None  # TODO: Implement
    ending_feed_rate: float = None  # TODO: Implement

    # How fast the print head should try to accelerate
    acceleration: float = 100
    starting_acceleration: float = None  # TODO: Implement
    ending_acceleration: float = None  # TODO: Implement

    # How much plastic to lay down
    line_width: float = 0.3
    layer_height: float = 0.1

    # How much length to extrude per mm traveled (mm/mm)
    flow_rate: float = None

    # Knob to turn if you want to do something weird
    flow_multiplier: float = 1

    filament_diameter: float = 1.75

    def __post_init__(self):
        if self.starting_feed_rate is None:
            self.starting_feed_rate = self.feed_rate
        if self.ending_feed_rate is None:
            self.ending_feed_rate = self.feed_rate

        if self.starting_feed_rate is None:
            self.starting_acceleration = self.acceleration
        if self.starting_feed_rate is None:
            self.ending_acceleration = self.acceleration

        if self.flow_rate is None:
            self.flow_rate = flow_rate(self.layer_height, self.line_width, self.filament_diameter)

    # @property
    # def feed_rate(self):
    #     return 60*self.feed_rate_mm


TEST_CONFIG = MoveConfig()

# If a move would move less than this amount in a direction, omit it from the Gcode
MOVE_EPSILON = 0.001


@dataclass
class Move:
    """
    A single move, generating a single G1 code

    Assumes that


    """

    start: OctoVector
    end: OctoVector
    extruding: bool = True
    config: MoveConfig = TEST_CONFIG

    comment: str = None

    def __post_init__(self):
        pass

    def checks(self):
        # TODO: check that the move doesn't go off the bed?
        pass

    def render(self, ):  # TODO: Crash if we're not there?
        delta = self.end - self.start
        distance = delta.norm()
        e = self.config.flow_rate * distance if self.config.is_extruding and self.extruding else \
            None
        out = ["G1"]
        if delta.x > MOVE_EPSILON or True:
            out.append(f"X{self.end.x:.6f}")
        if delta.y > MOVE_EPSILON or True:
            out.append(f"Y{self.end.y:.6f}")
        if delta.z > MOVE_EPSILON or True:
            out.append(f"Z{self.end.z:.6f}")
        if e is not None:
            out.append(f"E{e:.6f}")
        if self.config.feed_rate is not None:
            out.append(f"F{60 * self.config.feed_rate}")
        if self.comment is not None:
            out.append(f"; {self.comment}")
        return " ".join(out)


@dataclass
class Path:
    """
    Represents a series of moves that the printer will make before retracting


    """

    start: OctoVector
    default_move_config: MoveConfig = TEST_CONFIG

    moves: List[Move] = field(default_factory=list)
    is_closed: bool = False

    comment : str = None

    def __post_init__(self):
        self.print_head = self.start

    def move_to(self, end: OctoVector, config: MoveConfig, comment: str = None):
        start = self.start if len(self.moves) == 0 else self.moves[-1].end
        new_move = Move(start, end, config, comment)
        self.moves.append(new_move)

    def render(self):


        out = []

        move_to_start = Move(OctoVector(), self.start, extruding=False)

        pass


def test_move():
    move = Move(OctoVector(1, 2, 3), OctoVector(1, 2, 4))
    print(move.render())


if __name__ == "__main__":
    test_move()

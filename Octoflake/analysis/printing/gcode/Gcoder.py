import math
from dataclasses import dataclass, field
from typing import List, TextIO

from euclid3 import Vector2

from printing.gcode.Move import Move
from printing.gcode.Print import Layer, Print
from printing.gcode.TempConfig import TempConfig
from printing.grid.OctoVector import OctoVector



@dataclass
class GCoder:
    """"""

    # Where is the print head right now
    location: OctoVector = OctoVector()

    temp: TempConfig = TempConfig()



    def print(self, print:Print, rapid_iteration=False):
        """Takes the printer from cold and without filament, to """



        pass

    def setup(self, rapid_iteration=False):



    def print_layer(self, layer:Layer):
        pass

    def move(self, move:Move): # x=None, y=None, z=None, e=None, f=None, comment=None):
        out = ["G1"]
        if x is not None:
            out.append(f"X{x}")
        if y is not None:
            out.append(f"Y{y}")
        if z is not None:
            out.append(f"Z{z}")
        if e is not None:
            out.append(f"E{e}")
        if f is not None:
            out.append(f"F{60 * f}")
        if comment is not None:
            out.append(f"; {comment}")
        self.write_line(" ".join(out))

        new_x = x if x is not None else self.location.x
        new_y = y if y is not None else self.location.y
        new_z = z if z is not None else self.location.z

        self.location = OctoVector(new_x, new_y, new_z)

    def retract(self):

    def move_to(self, end: OctoVector, feedrate_mm_s: float = None):
        if feedrate_mm_s is None:
            feedrate_mm_s = self.travel_speed
        self.write_line(f"G1 X{end.x} Y{end.y} Z{end.z} F{60 * feedrate_mm_s}")
        self.location = end

    def extrude(self, end, feedrate_mm_s: float = None, flow: float = None):
        if flow is None:
            flow = flow_rate(self.layer_height, self.line_width)
        print(self.location, end)
        to_extrude = flow * end.distance(self.location)
        if feedrate_mm_s is None:
            feedrate_mm_s = self.extrusion_speed
        self.write_line(f"G1 X{end.x} Y{end.y} Z{end.z} E{to_extrude} F{60 * feedrate_mm_s}")

        self.location = end

    # TODO: Add acceleration control
    # def extrude_relative(self, dx = 0, dy = 0, feedrate_mm_s, ):

    # def

    def extrude_to(self):
        """Extrude to an absolute location"""

    def filament_move(distance_mm: float, feedrate_mm_s: float = 1, comment=""):  # TODO: comment
        return f"G1 E{distance_mm} F{60 * feedrate_mm_s}\n"


# TODO: Add a module for this
RAMMING = """G1 E2 F5000
G1 E2 F5500
G1 E2 F6000
G1 E-15.0000 F5800
G1 E-20.0000 F5500
G1 E10.0000 F3000
G1 E-10.0000 F3100
G1 E10.0000 F3150
G1 E-10.0000 F3250
G1 E10.0000 F3300"""







if __name__=="__main__":


    filenames = ["test.gcode", "/volumes/PRUSAI3MK3S/test.gcode"]

    gcoder = GCoder(filenames=filenames)


    config.movement_limit_config()
    config.checks()
    config.startup()
    config.purge()

    gcoder.move(x=50, y=50)
    gcoder.extrude(OctoVector(60, 50, 0))
    gcoder.extrude(OctoVector(60, 60, 0))
    gcoder.extrude(OctoVector(50, 60, 0))
    gcoder.extrude(OctoVector(50, 50, 0))

    config.shutdown()

    exit()

    print("wat")


def test_move():
    lines = []

    lines.append(section_title("Test movements"))
    lines.append(move(OctoVector(10, 10, 10)))
    location = OctoVector(10, 10, 10)
    for _ in range(10):

        next_location = OctoVector(20, 20, 10)
        lines.append(extrude(location, next_location))
        location = next_location

        next_location = OctoVector(10, 10, 10)
        lines.append(extrude(location, next_location))
        location = next_location

        # lines.append(extrude(OctoVector(20, 20, 10)))
        # lines.append(extrude(OctoVector(10, 20, 10)))
        # lines.append(extrude(OctoVector(20, 10, 10)))

    return lines


def make_square_spiral(x=100, y=100, n=10):
    r = 0
    out = []

    e = 0
    current = Vector2(x, y)
    next = Vector2(x, y)

    out.append(move(current))
    while r < n:
        # Assume we start at the bottom right

        r += 1
        next = current + Vector2(0, r)
        out.append(move(current, next))
        current = next

        next = current + Vector2(-r, 0)
        out.append(move(current, next))
        current = next

        r += 1

        next = current + Vector2(0, - r)
        out.append(move(current, next))
        current = next

        next = current + Vector2(r, 0)
        out.append(move(current, next))
        current = next

    return "\n".join(out)


# @dataclass
# class PurgeConfig:
#
#
#
#     def render(self):
#         lines = []
#         lines.append(section_title("Purge Line"))
#         lines.append()
#
#
#         return """
# ;go outside print area
# G1 Y-3.0 F1000.0
# G1 Z0.4 F1000.0
# ; select extruder
# Tc ; load filament to nozzle
#
# ; purge line
# G1 X55.0 F2000.0
# G1 Z0.3 F1000.0
# G92 E0.0
# G1 X240.0 E25.0 F1400.0
# G1 Y-2.0 F1000.0
# G1 X55.0 E25 F1400.0
# G1 Z0.20 F1000.0
# G1 X5.0 E4.0 F1000.0
#
# """


# @dataclass
# class PurgeLine:
#     printerConfig: MovementConfig = MovementConfig()
#
#     nozzle_line_width_multiplier: float = 2
#
#     def __post_init__(self):
#         pass
#
#     def render(self):
#         lines = []
#         lines.append(";;;;;;;; Purge Line ;;;;;;;;")
#         lines.append("G1 Y-3.0 F1000.0")
#
#         return "\n".join(lines)


MORE_SETTINGS = """
;TYPE:Custom
M862.3 P "MK3SMMU2S" ; printer model check
M862.1 P0.25 ; nozzle diameter check

G90 ; use absolute coordinates
M83 ; extruder relative mode
M104 S210 ; set extruder temp
M140 S30 ; set bed temp
Tx
M190 S30 ; wait for bed temp
M109 S210 ; wait for extruder temp
Tc

G28 W ; home all without mesh bed level


G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion


"""

if __name__ == "__main__":

    # config = PrinterConfig()

    # print(config.render())

    coder = Gcoder()
    print(coder.write_file("test.gcode"))
    print(coder.write_file("/volumes/PRUSAI3MK3S/test.gcode"))

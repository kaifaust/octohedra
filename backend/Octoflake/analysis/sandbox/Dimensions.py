import math
from pint import UnitRegistry
from collections import namedtuple


Flake = namedtuple("Flake", ['height', 'edge_length', 'triangle_height', 'diagonal', 'width'])

ureg = UnitRegistry()

FACE_LEAN = 2 * math.asin(1 / 2 / math.sin(math.radians(60)))




def from_edge_length(edge_length):
    triangle_height = edge_length * math.sin(math.radians(60))
    height = triangle_height * math.sin(FACE_LEAN)

    return edge_length, triangle_height, height

def from_height(height):
    triangle_height = max_height / math.sin(FACE_LEAN)
    edge_length = triangle_height / math.sin(math.radians(60))
    return edge_length, triangle_height, height


max_height = 30 * ureg.inch




max_triangle_height = max_height / math.sin(FACE_LEAN)
max_edge_length = max_triangle_height / math.sin(math.radians(60))
print(edge_length, triangle_height, height)










max_overall_edge_length = 36 *
print(max_overall_edge_length)

edge_length = 8 * ureg.centimeter
node_diameter = 1 * ureg.inch
weld_allowance = 1 * ureg.millimeter

flake_length = 8

total_edge_length = max_overall_edge_length - flake_length * 2 * weld_allowance - (flake_length + 1) * node_diameter

print(total_edge_length)
print((total_edge_length / flake_length).to("cm"))







from_height(30)

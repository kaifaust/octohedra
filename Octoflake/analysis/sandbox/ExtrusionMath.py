import math

import numpy as np


# area = (w - h) * h + pi * (h / 2) ** 2
#      = w * h - h ** 2 + pi * h ** 2 / 4
#    0  = (pi / 4 - 1) * h **2 + w * h - area # Lol quadratic equation

# a = (pi - 4) / 4
# b = w
# c = -area

# x = -b ± sqrt( b **2 -4 * a * c) / (2 * a)

# h = -w ± sqrt( w ** 2 - 4 * (pi - 4) / 4 * -area) / (2 * (pi - 4) / 4)
# h = -w ± sqrt( w ** 2 + (pi - 4)) / ((pi - 4)/2)

# x = -w ± w / ((pi / 2 - 2)
# h = -2 * w / ((pi - 4)/2)
# h = -4 * w / (pi - 4)


# area = w * h - h ** 2 + pi * h ** 2 / 4
# -w * h = -area - h ** 2 + pi * h ** 2 / 4
# w * h = area + h ** 2 - pi * h ** 2 / 4
# w = area / h + h - pi * h / 4

def get_target_width(nozzle_diameter, layer_height, extrusion_multiplier=1.0, flow_ratio=1.0):
    nozzle_radius = nozzle_diameter / 2
    raw_area = math.pi * (nozzle_radius ** 2)
    area = adjusted_area = raw_area / extrusion_multiplier * flow_ratio
    h = layer_height
    return area / h + h - math.pi * h / 4


def get_target_height(nozzle_diameter, line_width):
    nozzle_radius = nozzle_diameter / 2
    area = math.pi * (nozzle_radius ** 2)
    w = line_width
    print(line_width, w ** 2, (pi - 4))
    return -w + math.sqrt(w ** 2 - pi + 1) / (2 * (math.pi / 4 - 1))


def achieve_target_ratio(nozzle_diameter, ratio):
    pass


nd = 0.2
pi = math.pi

# np.linspace
# for height in (np.linspace(.15, .25, 21)):
for height in (0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2):
    # width = get_target_width(nd, height, extrusion_multiplier=1.25, flow_ratio=1.5)
    width = get_target_width(nd, height, extrusion_multiplier=0.95, flow_ratio=0.9)
    ratio = width / height
    print(f"{height:.3f}, {width:.4f}, {ratio:.4f}")

exit()

# for width in (.21, .25, .28):
#     print(width, get_target_height(nd, width))


############################## Old math


# area / h ** 2 = w / h - 1 + pi / 4
# area / h ** 2 + 1 - pi / 4 = w / h
# area / h + h - pi * h / 4 = w


##################### Stacking cylinders
for h in (np.arange(.1, .2, 0.005)):
    c_r = h * math.sqrt(2) / 2
    a = math.pi * c_r ** 2
    w = a / h + h - math.pi * h / 4
    print(f"{h=:.3f}, {c_r=:.4f}, {a=:.4f}, {w:.4f}")

h = 0.1
c_r = h * math.sqrt(2) / 2
a = math.pi * c_r ** 2

w = a / h + h - math.pi * h / 4

print(h, c_r, a, w)

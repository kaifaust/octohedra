import math

from solid import *



# d = union()(
#
#     sphere(15)
# )
#
#
# sectors = set()
#
# sectors.add(cube(10))
# sectors.add(translate((0, 0, 10))(cube(10)))
#
#
#
#
#
#
#
# e = [cube(10), sphere(10)]
#
#
# #print(scad_render(d))
#
#
#
# rendered = [scad_render(x) for x in sectors]
#
#
#
# with open("render.scad","w") as render:
#     render.writelines(rendered)
#
#
# from collections import namedtuple
# Config = namedtuple("Config", ['size', "iteration", "overlap", slit])

sqrt2 = math.sqrt(2)
sqrt22 = sqrt2 / 2

modules = import_scad("octomodules.scad")







# class Octo:
#
#     def __init__(self, size, iteration, overlap, slit, center, is_pyramid, neighbors):
#         self.size = size
#         self.iteration = iteration
#         self.overlap = overlap
#         self.slit = slit
#         self.center = center
#         self.is_pyramid = is_pyramid
#         self.neighbors = neighbors
#
#
#
#
#     def render(self, output_set):
#         if self.iteration == 0:
#             pass
#
#
#
#
#     def __eq__(self, other):
#         return self.center == other.center
#
#     def __str__(self):
#         pass



from collections import namedtuple



Octo = namedtuple("Octo", [
    "size",
    "center",
    "is_pyramid",
    "trim_front",
    "trim_back",
     "trim_left",
      "trim_right",
     "trim_top",
   "trim_bottom"
])

Trims = namedtuple("Trims", ["top", "bottom", "left", "right", "front", "back"])
NO_TRIMS = Trims(False, False, False, False, False, False)


def additive_octo(
        size=100.,
        iteration=3.,
        overlap=0.0,
        slit=0.0,
        center=(0, 0, 0),
        shapes=None,
        is_pyramid=False,
        trim_front=0,
        trim_back=0,
        trim_left=0,
        trim_right=0,
        trim_top=0,
        trim_bottom=0

):
    if iteration == 0:

        old_center = center
        center = tuple(map(lambda x: round(x, 5), center))

        if center in shapes:
            trim_front = max(trim_front, shapes[center].trim_front)
            trim_back = max(trim_back, shapes[center].trim_back)
            trim_left = max(trim_left, shapes[center].trim_front)
            trim_right = max(trim_right, shapes[center].trim_right)
            trim_top = max(trim_top, shapes[center].trim_top)
            trim_bottom = max(trim_bottom, shapes[center].trim_bottom)


        shapes[center] = Octo(
                size + 2 * overlap,
                center,
                is_pyramid,
                trim_front,
                trim_back,
                trim_left,
                trim_right,
                trim_top,
                trim_bottom
            )
        return None

    s2 = size / 2
    s4 = size / 4
    i1 = iteration - 1
    trim = overlap + slit/2

    # Front Left
    additive_octo(
        s2, i1, overlap, slit,
        (center[0] - s4, center[1] - s4, center[2]),
        shapes, is_pyramid,
        trim_front = trim_front, trim_back=trim, trim_left=trim_left, trim_right=trim, trim_top=0, trim_bottom=0
    )

    # Front Right
    additive_octo(
        s2, iteration - 1, overlap, slit,
        (center[0] + s4, center[1] - s4, center[2]),
        shapes, is_pyramid=is_pyramid,
        trim_front = trim_front, trim_back=trim, trim_left=trim, trim_right=trim_right, trim_top=0, trim_bottom=0
    )

    # Back Left
    additive_octo(
        s2, iteration - 1, overlap, slit,
        (center[0] - s4, center[1] + s4, center[2]),
        shapes, is_pyramid=is_pyramid,
        trim_front = trim, trim_back=trim_back, trim_left=trim_left, trim_right=trim, trim_top=0, trim_bottom=0
    )

    # Back Right
    additive_octo(
        s2, iteration - 1, overlap, slit,
        (center[0] + s4, center[1] + s4, center[2]),
        shapes, is_pyramid=is_pyramid,
        trim_front = trim, trim_back=trim_back, trim_left=trim, trim_right=trim_right, trim_top=0, trim_bottom=0
    )

    # Top
    additive_octo(
        s2, iteration - 1, overlap, slit,
        (center[0], center[1], center[2] + s4 * sqrt2),
        shapes, is_pyramid=False,
        trim_front = 0, trim_back=0, trim_left=0, trim_right=0, trim_top=trim_top, trim_bottom=overlap * sqrt2 if is_pyramid else 0
    )

    # Bottom
    if not is_pyramid:
        additive_octo(
            s2, iteration - 1, overlap, slit,
            (center[0], center[1], center[2] - s4 * sqrt2),
            shapes, is_pyramid=False,
            trim_front = 0, trim_back=0, trim_left=0, trim_right=0, trim_top=0, trim_bottom=trim_bottom
        )




def implicit_union_render(shapes, filename="render.scad"):
    # ren = [scad_render(x) for x in shapes]
    with open(filename, "w") as render_file:
        render_file.write("use </Users/silver/Desktop/Octoflake/analysis/printing/octomodules.scad>")
        for _, shape in shapes.items():
            scad_shape = translate(shape.center)(
                modules.octahedron(
                    shape.size,
                    trim_front = shape.trim_front,
                    trim_back = shape.trim_back,
                    trim_left = shape.trim_left,
                    trim_right = shape.trim_right,
                    trim_top=shape.trim_top,
                    trim_bottom=shape.trim_bottom,



                    is_pyramid=shape.is_pyramid,

                )
            )
            for line in scad_render(scad_shape).split("\n"):
                if not line.startswith("use"):
                    # print(line)
                    render_file.writelines(line + "\n")


        # render_file.writelines(lines)


def stellate(center, size, iteration, overlap, slit, shapes):
    center1 =(center[0] + size/2, center[1] + size/2, center[2])
    center2 =(center[0] + size/2, center[1] - size/2, center[2])
    center3 =(center[0] - size/2, center[1] + size/2, center[2])
    center4 =(center[0] - size/2, center[1] - size/2, center[2])
    center5 =(center[0], center[1], center[2] + sqrt22 * size)
    additive_octo(size/2, iteration-1, overlap, slit, center=center1, shapes=shapes, is_pyramid=True)
    additive_octo(size/2, iteration-1, overlap, slit, center=center2, shapes=shapes, is_pyramid=True)
    additive_octo(size/2, iteration-1, overlap, slit, center=center3, shapes=shapes, is_pyramid=True)
    additive_octo(size/2, iteration-1, overlap, slit, center=center4, shapes=shapes, is_pyramid=True)
    additive_octo(size/2, iteration-1, overlap, slit, center=center5, shapes=shapes, is_pyramid=False)



pyramid_size = 2


iteration = 5
size = pyramid_size * 2 ** iteration
overlap =.25
slit = .001

print(size)



shapes = dict()


additive_octo(size, iteration, overlap, slit, center=(0,0,0), shapes=shapes, is_pyramid=True)



stellate((0, 0, 0), size, iteration, overlap, slit, shapes)
stellate((size/2, size/2, 0), size/2, iteration-1, overlap, slit, shapes)
stellate((-size/2, size/2, 0), size/2, iteration-1, overlap, slit, shapes)
stellate((size/2, -size/2, 0), size/2, iteration-1, overlap, slit, shapes)
stellate((-size/2, -size/2, 0), size/2, iteration-1, overlap, slit, shapes)


additive_octo(size/4, iteration-2, overlap, slit, center=(0,0,sqrt22  * size + sqrt22 * size/2), shapes=shapes, is_pyramid=False)


# additive_octo(size/2, iteration-1, overlap, slit, center=(size/2,size/2,0), shapes=shapes, is_pyramid=True)







# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2, size/2, sqrt22 * size/2), shapes=shapes, is_pyramid=False)
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2 + size/4, size/2 + size/4, 0), shapes=shapes, is_pyramid=True)
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2 - size/4, size/2 + size/4, 0), shapes=shapes, is_pyramid=True)
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2 + size/4, size/2 - size/4, 0), shapes=shapes, is_pyramid=True)
#
# additive_octo(size/4, iteration-2, overlap, slit, center=(size/2, size/2, -sqrt22 * size/2), shapes=shapes, is_pyramid=False)
# additive_octo(size/4, iteration-2, overlap, slit, center=(size/2 + size/4, -size/2 + size/4, 0), shapes=shapes, is_pyramid=True)
# additive_octo(size/4, iteration-2, overlap, slit, center=(size/2 - size/4, -size/2 + size/4, 0), shapes=shapes, is_pyramid=True)
# additive_octo(size/4, iteration-2, overlap, slit, center=(size/2 + size/4, -size/2 - size/4, 0), shapes=shapes, is_pyramid=True)
#
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2, size/2, sqrt22 * size/2), shapes=shapes, is_pyramid=False)
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2 + size/4, size/2 + size/4, 0), shapes=shapes, is_pyramid=True)
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2 - size/4, size/2 + size/4, 0), shapes=shapes, is_pyramid=True)
# additive_octo(size/4, iteration-2, overlap, slit, center=(-size/2 + size/4, size/2 - size/4, 0), shapes=shapes, is_pyramid=True)

# print(shapes)



# lines = "\n".join([scad_render(x) for x in shapes])

# print(lines)
implicit_union_render(shapes)

# import math
# from dataclasses import astuple
# from functools import reduce
#
# from trimesh import Trimesh, util, transformations
# from trimesh.exchange.export import export_mesh
#
# from printing.builders.FlakeBuilder import FlakeBuilder
# from printing.grid.OctoCell import OctoCell
# from printing.grid.OctoGrid import OctoGrid
# from printing.grid.OctoVector import OctoVector
# from printing.utils import OctoConfigs
#
#
# class Renderer:
#
#     def __init__(self):
#         self.cache = dict()
#
#     def render(self, grid: OctoGrid, config=OctoConfigs.config_25):
#
#         cells = [self.render_cell(cell, center, config) for center, cell in grid.occ.items()]
#
#         # noinspection PyTypeChecker
#         mesh = util.concatenate(cells)
#
#         angle = math.radians(45)
#         rot = transformations.rotation_matrix(angle, (0, 0, 1))
#         mesh.apply_transform(rot)
#
#         return mesh
#
#     def render_cell(self, cell: OctoCell, center: OctoVector, config):
#         if astuple(cell) not in self.cache:
#             self.cache[astuple(cell)] = cell.render(config).remove_degenerate_faces()
#
#         return self.cache[astuple(cell)].copy().apply_translation(center * (config.cell_size / 4))
#
#
#
#
# if __name__ == "__main__":
#
#     r = Renderer()
#
#     grid = OctoGrid()
#     # grid.insert_cell(OctoVector(0,0,0))
#     grid = FlakeBuilder(1).materialize()
#
#
#     grid.crop_bottom()
#     grid.compute_trimming()
#     # grid.occ[OctoVector(0,0,0)].trim_ne = True
#     # grid.occ[OctoVector(0,0,0)].trim_nw = True
#     # grid.occ[OctoVector(0,0,0)].trim_sw = True
#     # # grid.occ[OctoVector(0,0,0)].trim_se = True
#     rendered = r.render(grid)
#
#     rendered.remove_duplicate_faces()
#     rendered.remove_unreferenced_vertices()
#     rendered.remove_degenerate_faces()
#
#     print("water", rendered.is_watertight)
#
#     # rendered.faces = rendered.faces + [rendered.faces[0]]
#
#     # rendered.triangles = rendered.triangles + [rendered.triangles[-1]]
#
#     # print(rendered.vertices)
#     # print(rendered.faces)
#
#
#
#     # export_mesh(rendered, f"/users/Silver/Desktop/shapes/cellderp.obj", include_normals=False,
#     # digits=10)
#
#     filename = f"/users/Silver/Desktop/shapes/cellderp.obj"
#     with open(filename, "w") as f:
#         print(export_mesh(rendered, None, file_type="obj", include_normals=False, digits=10),
#               file=f)
#     # export_mesh(rendered, f"/users/Silver/Desktop/shapes/cellderp.stl")

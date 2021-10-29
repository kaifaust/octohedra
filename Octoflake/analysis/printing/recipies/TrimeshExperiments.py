import trimesh
from trimesh import Trimesh, creation
from trimesh.exchange.export import export_mesh

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.TowerBuilders import EvilTower
from printing.grid.OctoCell import OctoCell
from printing.grid.Renderer import Renderer
from printing.utils import OctoConfigs
from printing.utils.RenderUtils import render_grid

box = trimesh.primitives.Box()

# print(box.vertices)
# print(box.faces)


# def np_mesh_to_trimesh(mesh):
#     np.fla

# old_mesh = OctoCell().render(OctoConfigs.config_25)
# points = list(set(map(tuple, old_mesh.vectors.reshape((-1, 3)))))
#
# point_dict = {point: i for i, point in enumerate(points)}
#
# faces = []
# for p1, p2, p3 in old_mesh.vectors:
#     faces.append(
#             (point_dict[tuple(p1)],
#              point_dict[tuple(p2)],
#              point_dict[tuple(p3)]
#              ))





# octo = Trimesh(points, faces)

# grid = FlakeBuilder(3).materialize()
# grid.crop_bottom()
# grid.compute_trimming()
#
# # octo = OctoCell().render_trimesh(OctoConfigs.config_25)
# octo = grid.render_trimesh(OctoConfigs.config_25_double_bottom)
#
#
#
# octo = creation.cylinder(10, 10)
# octo.apply_translation()
#
# poses, odds = octo.compute_stable_poses()
#
#
# for i, pose in enumerate(zip(poses, odds)):
#     transform, odds = pose
#     export_mesh(octo.apply_transform(transform), f"/users/Silver/Desktop/shapes/triderp_{odds}.obj")
#
# print(octo.is_watertight, octo.is_winding_consistent, )
# exit()
#
#
# export_mesh(octo, "/users/Silver/Desktop/shapes/triderp.obj")
#
# render_grid(grid,base_filename="old_way", z_min=None, config=OctoConfigs.config_25_double_bottom)
#
#
#
# print("hi")


grid = EvilTower(4).materialize()
grid.crop_bottom()
grid.compute_trimming()




for width, height in ((.23, .11), (.24,.13), (0.26, .15)):

    config = OctoConfigs.config_25_double_bottom
    config.absolute_line_width = width
    config.absolute_layer_height = height
    config.absolute_layers_per_cell = 6
    config.line_overlap = .99
    config.derive()


    mesh = Renderer().render(grid, config=config)

    filename = f"/users/Silver/Desktop/shapes/derp_{width}_{height}.obj"

    export_mesh(mesh, filename, include_normals=False)

    with open(filename, "a") as f:
        f.write("\n")

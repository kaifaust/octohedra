import trimesh
from trimesh.exchange.export import export_mesh

from printing.builders.TowerBuilders import EvilTower
from printing.grid.Renderer import Renderer
from printing.utils.OctoConfig import OctoConfig

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
#     export_mesh(octo.apply_transform(transform), f"/users/Silver/Desktop/shapes/triderp_{
#     odds}.obj")
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


config = OctoConfig(
        name="0.25mm nozzle, double bottom",
        nozzle=0.25,
        absolute_line_width=0.30,
        absolute_layer_height=0.15,
        first_layer_multiplier=1.5,
        # absolute_overlap= overlap,
        solid_layers=1,
        absolute_layers_per_cell=10,
        absolute_slit=0.001
        )

for i in range(1, 7):
    # for height, width in ((.15, .3), (.15, .45), (.2, .3)):
    # for layers in (4, 5, 6, 7, 8):

    grid = EvilTower(i, elevate_base=True, contact_patch_i_offset=1).materialize()
    grid.crop_bottom()
    grid.compute_trimming()

    # config = OctoConfigs.config_25_double_bottom
    # config.absolute_line_width = width
    # config.absolute_layer_height = height
    config.absolute_layers_per_cell = layers = 5

    # config.absolute_overlap = 2.99 * height
    config.line_overlap = .99

    config.derive()
    config.print_settings()
    config.print_derived_values()

    mesh = Renderer().render(grid, config=config)

    filename = f"/users/Silver/Desktop/shapes/derp_i{i}.obj"
    # filename = f"/users/Silver/Desktop/shapes/derp_{layers}.obj"
    # filename = f"/users/Silver/Desktop/shapes/derp_{layers}.obj"
    # filename = f"/users/Silver/Desktop/shapes/derp_{width}_{height}.obj"

    export_mesh(mesh, filename, include_normals=False)

    with open(filename, "a") as f:
        f.write("\n")

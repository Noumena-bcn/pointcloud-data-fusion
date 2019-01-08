import numpy as np
from pyntcloud import PyntCloud
import pandas as pd

# anky = PyntCloud.from_file("data/fused.ply")
# print (anky)
#
# #install IPython
# anky.plot(mesh=True, backend="threejs")
#
# voxelgrid_id = anky.add_structure("voxelgrid", n_x=20, n_y=20, n_z=20)
# voxelgrid = anky.structures[voxelgrid_id]
# voxelgrid.plot(d=3, mode="density", cmap="hsv")
#
# #install ipywidgets and pythreejs
# inclination_degrees = anky.add_scalar_field("inclination_degrees")
# anky.plot(use_as_color=inclination_degrees, cmap="jet")



cloud = PyntCloud.from_file("data/fused.ply")

# cloud.add_scalar_field("hsv")

voxelgrid_id = cloud.add_structure("voxelgrid", n_x=100, n_y=100, n_z=100)

new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)

new_cloud.to_file("out_file.npz")

print (new_cloud)

new_cloud.plot(mesh=True, backend="threejs")
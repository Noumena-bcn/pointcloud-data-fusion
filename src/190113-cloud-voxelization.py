import numpy as np
from pyntcloud import PyntCloud
import csv
import pandas as pd

#############################################################
# VOXEL CLOUD

# open cloud
cloud = PyntCloud.from_file("data/fused.ply")
print(cloud)

# voxel grid size
n_x= 100
n_y= 100
n_z= 100

# voxelized cloud
voxelgrid_id = cloud.add_structure("voxelgrid", n_x=100, n_y=100, n_z=100)
voxelgrid_centers = cloud.get_sample("voxelgrid_centers", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
voxelgrid_nearest = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
print(voxelgrid_centers)
# print(voxelgrid_nearest)

# voxelgrid_centers.to_file("out_file.npz")

# print(voxelgrid_centers.points.columns)
# print(voxelgrid_nearest.points.columns)


# # # # # # # # # # # # # # # # # # # # # # # # # #
# print(voxelgrid_nearest.points.columns)
voxelgrid_centers_df = voxelgrid_centers.points
voxelgrid_nearest_df = voxelgrid_nearest.points

voxelgrid_centers_df['nx'] = pd.Series(voxelgrid_nearest_df['nx']).values
voxelgrid_centers_df['ny'] = pd.Series(voxelgrid_nearest_df['ny']).values
voxelgrid_centers_df['nz'] = pd.Series(voxelgrid_nearest_df['nz']).values

voxelgrid_centers_df['red'] = pd.Series(voxelgrid_nearest_df['red']).values
voxelgrid_centers_df['green'] = pd.Series(voxelgrid_nearest_df['green']).values
voxelgrid_centers_df['blue'] = pd.Series(voxelgrid_nearest_df['blue']).values

voxelgrid_centers_df['voxel_n(V([100, 100, 100],[None, None, None],True))'] = pd.Series(voxelgrid_nearest_df['voxel_n(V([100, 100, 100],[None, None, None],True))']).values

print(voxelgrid_centers)
voxelgrid_centers.to_file("out_file.npz")

voxelgrid_centers.plot(mesh=True, backend="threejs")

# # cloud to csv
# # print(cloud.points)
df = voxelgrid_centers.points
# write csv
f = open('csvfile-voxels.csv','w')
df.to_csv(f)

dfnear = voxelgrid_nearest.points
# write csv
cnear = open('csvfile-nearest.csv','w')
dfnear.to_csv(cnear)



#############################################################

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


#############################################################
# # CLOUD DATA

# # open cloud
# cloud = PyntCloud.from_file("data/fused.ply")
# print(cloud)
#
# # export cloud to threesj
# cloud.plot(mesh=True, backend="threejs")
#
# # cloud to csv
# print(cloud.points)
# df = cloud.points
# # write csv
# f = open('csvfile.csv','w')
# df.to_csv(f)
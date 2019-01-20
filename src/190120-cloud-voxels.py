# Script to read/save Pointcloud data + normalize/save Normalize Pointcloud data
# #install IPython " ipywidgets and pythreejs

import numpy as np
from pyntcloud import PyntCloud
import csv
import pandas as pd
import matplotlib as mpl

# ############################################################
# # RGB CLOUD DATA
#
# # open cloud
# cloud = PyntCloud.from_file("data/ply/ok-fused-rgb-1000.ply")
# print(cloud)
#
# # export cloud to threesj
# cloud.plot(mesh=True, backend="threejs")
#
# # cloud to csv
# # print(cloud.points)
# df = cloud.points
# # write csv
# f = open('csvfile.csv','w')
# df.to_csv(f)

# #############################################################
# VOXEL CLOUD DATA

# open cloud
cloud = PyntCloud.from_file("data/ply/ok-fused-thermal-1000.ply")
# print(cloud)

# voxel grid size
# n_x= 100
# n_y= 100
# n_z= 100

# voxelized cloud
voxelgrid_id = cloud.add_structure("voxelgrid", n_x=500, n_y=500, n_z=500)
voxelgrid_centers = cloud.get_sample("voxelgrid_centers", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
voxelgrid_nearest = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
print(voxelgrid_centers)


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # ADD COLORS COLUMNS to centers voxels from nearest voxels
print(voxelgrid_nearest.points.columns)
voxelgrid_centers_df = voxelgrid_centers.points
voxelgrid_nearest_df = voxelgrid_nearest.points

print(voxelgrid_nearest_df.head(10))
voxelgrid_nearest_df = voxelgrid_nearest.points.sort_values(by=['x', 'y','z'])
print(voxelgrid_nearest_df.head(10))

#
# # voxelgrid_centers_df['nx'] = pd.Series(voxelgrid_nearest_df['nx']).values
# # voxelgrid_centers_df['ny'] = pd.Series(voxelgrid_nearest_df['ny']).values
# # voxelgrid_centers_df['nz'] = pd.Series(voxelgrid_nearest_df['nz'].values
#
voxelgrid_centers_df['red'] = pd.Series(voxelgrid_nearest_df['red']).values
voxelgrid_centers_df['green'] = pd.Series(voxelgrid_nearest_df['green']).values
voxelgrid_centers_df['blue'] = pd.Series(voxelgrid_nearest_df['blue']).values

print(voxelgrid_centers)
#
# #############################################################
# SAVE CLOUD

voxelgrid_centers.to_file("out_file.npz")
voxelgrid_centers.plot(mesh=True, backend="threejs")

# # cloud to csv
# # print(cloud.points)
df = voxelgrid_centers_df
# write csv
f = open('csvfile-voxels.csv','w')
df.to_csv(f)

dfnear = voxelgrid_nearest_df
# write csv
cnear = open('csvfile-nearest.csv','w')
dfnear.to_csv(cnear)

















#############################################################

# green_boolean = voxelgrid_centers.points["green"] > 200
#
# booleans = []
#
# for value in voxelgrid_centers.points["green"]:
#     if value >= 200:
#         booleans.append(True)
#     else:
#         booleans.append(False)
#
# Green_Value = pd.Series(booleans)
# print (Green_Value.head())
# print (voxelgrid_centers.points[Green_Value])
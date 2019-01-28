# Script to read/save Pointcloud data + normalize/save Normalize Pointcloud data
# #install IPython " ipywidgets and pythreejs

import numpy as np
from pyntcloud import PyntCloud
from scipy.spatial.distance import cdist

import csv
import pandas as pd
import matplotlib as mpl

# #############################################################
# VOXEL CLOUD DATA

# open cloud
cloud = PyntCloud.from_file("data/ply/P9-data-fusion-term-180726.ply")
# print(cloud)

# voxel grid size
# n_x= 100
# n_y= 100
# n_z= 100

# voxelized cloud
voxelgrid_id = cloud.add_structure("voxelgrid", n_x=200, n_y=200, n_z=200)
voxelgrid_nearest = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
voxelgrid_centers = cloud.get_sample("voxelgrid_centers", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)

# print(voxelgrid_centers)


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# CALCULATE NEAREST POINT
# define function for closest point and match values
def closest_point(point, points):
    """ Find closest point from a list of points. """
    return points[cdist([point], points).argmin()]

def match_value(df, col1, x, col2):
    """ Match value x from col1 row to value in col2. """
    return df[df[col1] == x][col2].values[0]

# define dataframe
df1 = voxelgrid_nearest.points
df2 = voxelgrid_centers.points
print("----------------DATAFRAME----------------")
print(df2.head(5))
print(df2.columns)

# extract values from x y z for each point on both lists
df1['point'] = [(x, y, z) for x,y,z in zip(df1['x'], df1['y'], df1['z'])]
df2['point'] = [(x, y, z) for x,y,z in zip(df2['x'], df2['y'], df2['z'])]

# find closest point
df2['closest'] = [closest_point(x, list(df1['point'])) for x in df2['point']]

# add columns for r g b
df2['red'] = [match_value(df1, 'point', x, 'red') for x in df2['closest']]
df2['green'] = [match_value(df1, 'point', x, 'green') for x in df2['closest']]
df2['blue'] = [match_value(df1, 'point', x, 'blue') for x in df2['closest']]

# erase addittional columns point and closest
columns = ['point', 'closest']
print("----------------ERASE COLUMN----------------")
voxelgrid_centers.points = voxelgrid_centers.points.drop(columns, axis=1)
print(voxelgrid_centers.points.head(5))
print(voxelgrid_centers.points.columns)


#############################################################
# SAVE CLOUD
print("----------------PRINT DATA STRUCTURE----------------")
print(voxelgrid_centers)
print(voxelgrid_centers.points.columns)

# output data to threejs
voxelgrid_centers.to_file("out_file.npz")
voxelgrid_centers.plot(mesh=True, backend="threejs")

# cloud to csv
df = voxelgrid_centers.points
# write csv
f = open('csvfile-centers.csv','w')
df.to_csv(f)


# # cloud to csv
# df = voxelgrid_nearest.points
# # write csv
# f = open('csvfile-nearest.csv','w')
# df.to_csv(f)


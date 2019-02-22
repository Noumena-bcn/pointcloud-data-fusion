# FILE TO CLUSTERS POINT CLOUDS ACCORDING TO THE GREEN VALUES
# FOR GENERAL REFERENCE: https://github.com/SonyCSLParis/GlobalSummerSchool18/blob/master/notebooks/segmentation.ipynb

from pyntcloud import PyntCloud


# RGB CLOUD DATA

# open cloud
cloud = PyntCloud.from_file("data/fused.ply")
# print(cloud)
# print(cloud.points)


# green_boolean = cloud.points["green"] <150
# cloud.points = (cloud.points[green_boolean])


# print(cloud.points[cloud.points["green"] <150],  cloud.points[cloud.points["red"] <150],  cloud.points[cloud.points["blue"] <150])

# green_boolean = cloud.points["green"].between(200,255, inclusive=False)
# cloud.points = (cloud.points[green_boolean])

# # MULTIPLE ROWS
# print(cloud.points[(cloud.points['red']>10) & (cloud.points['green']>100) & (cloud.points['blue']>100)])

# MULTIPLE ROWS RANGE
cloud.points = cloud.points[(cloud.points["red"].between(100,255, inclusive=False)) & (cloud.points["green"].between(100,255, inclusive=False)) & (cloud.points["blue"].between(100,255, inclusive=False))]




# # SAVE CLOUD TO THREEJS AND CSV
# export cloud to threesj
cloud.plot(mesh=True, backend="threejs")

# cloud to csv
print(cloud.points)
df = cloud.points
# write csv
f = open('csvfile.csv','w')
df.to_csv(f)




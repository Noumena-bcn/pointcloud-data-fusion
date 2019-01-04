from __future__ import print_function
import cv2
import numpy as np
import glob
import os
import rasterio
from rasterio.plot import show_hist
from rasterio.plot import show
import pathlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from osgeo import gdal, gdalconst
from sys import argv
import imutils


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# SETTING GRADIENT FOR NDVI COLORMAP
colors = [(0.019608,0.094118,0.321569),(0.019608,0.094118,0.321569), (0.019608,0.094118,0.321569),(1, 1, 1), (1, 1, 1),(1, 1, 1),(1, 1, 1),(0.74902, 0.647059, 0.494118),(0.529412, 0.721569, 0),(0, 0.45098, 0),(0, 0.45098, 0)]  # R -> G -> B
n_bins = 10  # Discretizes the interpolation into bins
cmap_name = 'my_list'


cm = LinearSegmentedColormap.from_list(
        cmap_name, colors, n_bins)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MATCHING IMAGES - HOMOGRAPHY
MAX_FEATURES = 10000
GOOD_MATCH_PERCENT = 0.02

# MATCHING FUNCTION
def alignImages(im1, im2):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    # cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LOOP INTO FOLDERS
# for subdir in glob.glob("/Volumes//N_1TB/agisoft-data/PT_8/DCIM/*"):
for subdir in glob.glob("/Volumes/N_1TB/agisoft-data/PT_6/DCIM/*"):
    nir_path = ""
    red_path = ""
    nirAligned = ""
    imReg = ""
    currentDirectory = pathlib.Path(subdir)
    print("////////////////////////////////")
    print(currentDirectory)

    red_current_pattern = '*RED.TIF'
    nir_current_pattern = '*NIR.TIF'
    # PROBLEM TO FIX WITGH THE LIST
    red_path_ = []
    nir_path_ = []
    for _nir in currentDirectory.glob(nir_current_pattern):
        nir_path_.append(_nir)

    for _red in currentDirectory.glob(red_current_pattern):
        red_path_.append(_red)

    print("Reading NIR image : ", nir_path_[0].name)
    print("Reading RED image : ", red_path_[0].name)

    nir_path = nir_path_[0]
    red_path = red_path_[0]
    # PROBLEM TO FIX WITH THE LIST

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # MATCHING
    imReference = cv2.imread(str(red_path), cv2.IMREAD_COLOR)
    print(imReference.shape, imReference.dtype)


    im = cv2.imread(str(nir_path), cv2.IMREAD_COLOR)
    print(im.shape, im.dtype)


    # ALIGN IMAGE
    print("Aligning images ...")
    # Registered image will be resotred in imReg.
    # The estimated homography will be stored in h.
    imReg, h = alignImages(im, imReference)
    # cv2.imshow("Before Rotation", imReg)
    # cv2.waitKey(0)

    # ROTATE IMAGE
    rotated = imutils.rotate_bound(imReg, 180)
    # cv2.imshow("Rotated", rotated)
    # cv2.waitKey(0)


    # WRITE ALIGNED IMAGE TO DISK
    nirName = os.path.basename(os.path.normpath(currentDirectory))
    nirPath = os.path.join(currentDirectory, nirName + '-NIR_.TIF')


    nirAligned = nirPath
    print("Saving aligned image : ", nirAligned)
    # print (imReg.shape, imReg.dtype)
    cv2.imwrite(nirAligned, rotated)
    print("Reading NEW NIR image : ", nirAligned)
    print(rotated.shape, rotated.dtype)




    # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # #
    # NDVI ANALYSIS - USE ALIGNED -NIR_.TIF IMAGE
    # gdal raster read
    print('/////////////// RED BANDS ////////////////////')
    dataset = gdal.Open(str(red_path), gdal.GA_Update)

    # Get RED band
    red_band = dataset.GetRasterBand(1)
    red_array = red_band.ReadAsArray()
    # print(red_array)

    # print('------------------')

    raster = rasterio.open(red_path)
    red = raster.read(1)
    # print(red)

    # Get NIR band
    # gdal raster read
    print('/////////////// NIR BANDS ////////////////////')
    dataset = gdal.Open(str(nirPath), gdal.GA_Update)

    # Get RED band
    nir_band = dataset.GetRasterBand(1)
    nir_array = nir_band.ReadAsArray() * 257
    # print(nir_array)

    # print('------------------')

    raster = rasterio.open(nirAligned)
    nir= raster.read(1) * 257
    # print(nir)


    #floating values
    red = (red_array/256).astype(float)
    nir = (nir_array/256).astype(float)


    #allow 0 division in numpy
    np.seterr(divide='ignore', invalid='ignore')

    #initialize ndvi calculation
    ndvi = np.empty(raster.shape, dtype=rasterio.float32)
    check = np.logical_or( red>0, nir>0)

    ndvi = np.where (check, (nir-red) / (nir+red), -999)
    
    ndviPath = '/Users/aldo/Desktop/ndvi/'
    ndviName = os.path.basename(os.path.normpath(currentDirectory))
    print(ndviName)

    # SAVE IMAGE PLT
    plt.imsave(ndviPath + ndviName + ".png", ndvi, cmap=cm)

    # # VISUALIZATION
    # # NDVI image
    # show(ndvi, cmap=cm)
    # # rasterio histogram of single or multiband raster:
    # show_hist(ndvi, bins=50, lw=0.0, stacked=False, alpha=0.8, histtype='stepfilled', title="Histogram")

    print('------------------')























































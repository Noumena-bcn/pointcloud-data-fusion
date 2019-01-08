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
# LOOP INTO FOLDERS
# for subdir in glob.glob("/Volumes//N_1TB/agisoft-data/PT_8/DCIM/*"):
for subdir in glob.glob("/Users/aldo/Desktop/DCIM/*"):
    nir_path = ""
    red_path = ""
    nirAligned = ""
    imReg = ""
    currentDirectory = pathlib.Path(subdir)
    print("////////////////////////////////")
    print(currentDirectory)

    rgb_current_pattern = '*RGB.JPG'
    red_current_pattern = '*RED.TIF'
    nir_current_pattern = '*NIR.TIF'
    # PROBLEM TO FIX WITH THE LIST
    rgb_path_ = []
    red_path_ = []
    nir_path_ = []
    for _rgb in currentDirectory.glob(rgb_current_pattern):
        rgb_path_.append(_rgb)

    for _nir in currentDirectory.glob(nir_current_pattern):
        nir_path_.append(_nir)

    for _red in currentDirectory.glob(red_current_pattern):
        red_path_.append(_red)

    # print("Reading RGB image : ", rgb_path_[0].name)
    # print("Reading NIR image : ", nir_path_[0].name)
    # print("Reading RED image : ", red_path_[0].name)

    nirImg= nir_path_[0]
    redImg = red_path_[0]
    print (nirImg)
    print (redImg)

    nirI = cv2.imread(str(nirImg))
    # cv2.imshow('test',nirI)
    # cv2.waitKey(0)

    cols = nirI.shape[1]
    rows = nirI.shape[0]
    M = np.float32([[1,0,-2],[0,1,17]])
    dst = cv2.warpAffine(nirI, M, (cols,rows))
    # cv2.imshow('img', dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # WRITE ALIGNED IMAGE TO DISK
    nirName = os.path.basename(os.path.normpath(currentDirectory))
    nirPath = os.path.join(currentDirectory, nirName + '-NIR_.TIF')

    # ROTATE IMAGE
    rotated = imutils.rotate_bound(dst, 180)


    nirAligned = nirPath
    print(nirAligned)
    print("Saving aligned image : ", nirAligned)
    # print (imReg.shape, imReg.dtype)
    cv2.imwrite(nirAligned, rotated)
    # print(dst.shape, dst.dtype)


    # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # #
    # NDVI ANALYSIS - USE TRANSLATED -NIR_.TIF IMAGE

    # Get RED band
    # gdal raster read
    dataset = gdal.Open(str(redImg), gdal.GA_Update)

    # Get RED band
    red_band = dataset.GetRasterBand(1)
    red_array = red_band.ReadAsArray()

    # Get NIR band
    # gdal raster read
    dataset = gdal.Open(str(nirPath), gdal.GA_Update)

    # Get RED band
    nir_band = dataset.GetRasterBand(1)
    nir_array = nir_band.ReadAsArray() * 257

    #floating values
    red = (red_array/256).astype(float)
    nir = (nir_array/256).astype(float)

    # allow 0 division in numpy
    np.seterr(divide='ignore', invalid='ignore')

    # initialize ndvi calculation
    ndvi = np.empty(dst.shape, dtype=rasterio.float32)
    check = np.logical_or(red > 0, nir > 0)

    ndvi = np.where(check, (nir - red) / (nir + red), -999)

    ndviPath = '/Users/aldo/Desktop/ndvi/'
    ndviName = os.path.splitext(rgb_path_[0].name)[0]
    print(ndviName)
    print(ndviPath)

    # SAVE IMAGE PLT
    save = plt.imsave(ndviPath + ndviName + ".JPEG", ndvi, cmap=cm)
    print (save)

    # VISUALIZATION
    # NDVI image
    show(ndvi, cmap=cm)





    # raster = rasterio.open(redImg)
    # red = raster.read(1)
    # print(red)
    #
    #
    # # Get NIR band
    # raster = rasterio.open(str(nirAligned))
    # nir= raster.read(1)
    # print (nir)
    #
    #
    # #allow 0 division in numpy
    # np.seterr(divide='ignore', invalid='ignore')
    #
    # #initialize ndvi calculation
    # ndvi = np.empty(raster.shape, dtype=rasterio.float32)
    # check = np.logical_or( red>0, nir>0)
    #
    # ndvi = np.where (check, (nir-red) / (nir+red), -999)
    #
    # ndviPath = '/Users/aldo/Desktop/ndvi/'
    # ndviName = os.path.splitext(rgb_path_[0].name)[0]
    # print(ndviName)
    #
    #
    # # SAVE IMAGE PLT
    # plt.imsave(ndviPath + ndviName + ".JPEG", ndvi, cmap=cm)
    #
    #
    # # VISUALIZATION
    # # NDVI image
    # show(ndvi, cmap=cm)
    # # # rasterio histogram of single or multiband raster:
    # # show_hist(ndvi, bins=50, lw=0.0, stacked=False, alpha=0.8, histtype='stepfilled', title="Histogram")
    #
    # print('------------------')
















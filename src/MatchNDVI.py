import glob
import os
import rasterio
import numpy as np
import pathlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from rasterio.plot import show
from matplotlib import cm
import matplotlib.colors as colors
from rasterio.plot import show_hist


colors = [(0.019608,0.094118,0.321569), (1, 1, 1), (1, 1, 1),(0.74902, 0.647059, 0.494118),(0.74902, 0.647059, 0.494118),(0.529412, 0.721569, 0),(0.529412, 0.721569, 0),(0, 0.45098, 0),(0, 0.45098, 0),(0, 0.45098, 0),(0, 0.45098, 0),(0, 0.45098, 0),(0, 0.45098, 0),(0, 0.45098, 0),(0, 0.45098, 0)]  # R -> G -> B
n_bins = 10  # Discretizes the interpolation into bins
cmap_name = 'my_list'


cm = LinearSegmentedColormap.from_list(
        cmap_name, colors, n_bins)


# for subdir in glob.glob("/Volumes//N_1TB/agisoft-data/PT_9/DCIM/*"):
for subdir in glob.glob("/Users/_starsky/Desktop/PT_8/*"):
    currentDirectory = pathlib.Path(subdir)
    print(currentDirectory)

    #filepath red
    currentPattern = '*RED.TIF'

    for raster in currentDirectory.glob(currentPattern):
        raster = rasterio.open(raster)
        print(raster)

        # reading bands
        red = raster.read(1)
        print(red)
        # show(red)

    # filepath nir
    currentPattern = '*-NIR.TIF'

    for raster in currentDirectory.glob(currentPattern):
        raster = rasterio.open(raster)
        print(raster)

        # reading bands
        nir = raster.read(1)
        print(nir)
        # show(nir)


        # floating values
        red = (red / 256).astype(float)
        nir = (nir / 256).astype(float)

        print(nir)

        # allow 0 division in numpy
        np.seterr(divide='ignore', invalid='ignore')

        # initialize ndvi calculation
        ndvi = np.empty(raster.shape, dtype=rasterio.float32)
        check = np.logical_or(red > 0, nir > 0)

        ndvi = np.where(check, (nir - red) / (nir + red), -999)
        print(ndvi)
        # show(np.logical_and(ndvi>0.2, ndvi<0.8), cmap="summer")
        # show(ndvi, cmap=cm)


        #save images in path
        # ndviPath = '/Volumes//N_1TB/agisoft-data/PT_9/NDVI/'
        ndviPath = '/Users/_starsky/Desktop/ndvi'
        ndviName = os.path.basename(os.path.normpath(currentDirectory))
        print(ndviName)


        plt.imsave(ndviPath+ndviName+".png", ndvi, cmap=cm)
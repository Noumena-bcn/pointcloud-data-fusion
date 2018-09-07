#! /usr/bin/env python

#######################################
# GDALCalcNDVI.py
#
# A script using the GDAL Library to
# create a new image contains the NDVI
# of the original image
#
# Author: <YOUR NAME>
# Email: <YOUR EMAIL>
# Date: DD/MM/YYYY
# Version: 1.0
#######################################

# Import required libraries from python
import sys, os, struct
# Import gdal
import osgeo.gdal as gdal


# Define the class GDALCalcNDVI
class GDALCalcNDVI (object):

    # A function to create the output image
    def createOutputImage(self, outFilename, inDataset):
        # Define the image driver to be used
        # This defines the output file format (e.g., GeoTiff)
        driver = gdal.GetDriverByName("GTiff")
        # Check that this driver can create a new file.
        metadata = driver.GetMetadata()
        if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
            print
            'Driver GTiff supports Create() method.'
        else:
            print
            'Driver GTIFF does not support Create()'
            sys.exit(-1)
        # Get the spatial information from the input file
        geoTransform = inDataset.GetGeoTransform()
        geoProjection = inDataset.GetProjection()
        # Create an output file of the same size as the inputted
        # image, but with only 1 output image band.
        newDataset = driver.Create(outFilename, inDataset.RasterXSize, inDataset.RasterYSize, 1, gdal.GDT_Float32)
        # Define the spatial information for the new image.
        newDataset.SetGeoTransform(geoTransform)
        newDataset.SetProjection(geoProjection)
        return newDataset

    # The function which loops through the input image and
    # calculates the output NDVI value to be outputted.
    def calcNDVI(self, filePathNIR, filePathRED, outFilePath):
        # Open the inputted dataset
        datasetNIR = gdal.Open(filePathNIR, gdal.GA_ReadOnly)
        datasetRED = gdal.Open(filePathRED, gdal.GA_ReadOnly)

        # Check the dataset was successfully opened
        if datasetNIR  is None:
            print("The dataset could not opened, datasetNIR")
            sys.exit(-1)
        if datasetRED is None:
            print("The dataset could not opened, datasetRED")
            sys.exit(-1)

        # # Create the output dataset
        # outDataset = self.createOutputImage(outFilePath, datasetNIR, datasetRED)
        # # Check the datasets was successfully created.
        # if outDataset is None:
        #     print('Could not create output image')
        #     sys.exit(-1)

        # Get hold of the RED and NIR image bands from the image
        # Note that the image bands have been hard coded
        # in this case for the Landsat sensor. RED = 3
        # and NIR = 4 this might need to be changed if
        # data from another sensor was used.
        red_band = datasetNIR.GetRasterBand(1)  # RED BAND
        nir_band = datasetRED.GetRasterBand(1)  # NIR BAND
        # Retrieve the number of lines within the image
        numLines = red_band.YSize
        # Loop through each line in turn.
        for line in range(numLines):
            # Define variable for output line.
            outputLine = ''
            # Read in data for the current line from the
            # image band representing the red wavelength
            red_scanline = red_band.ReadRaster(0, line, red_band.XSize, 1, red_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            red_tuple = struct.unpack('f' * red_band.XSize, red_scanline)

            # Read in data for the current line from the
            # image band representing the NIR wavelength
            nir_scanline = nir_band.ReadRaster(0, line, nir_band.XSize, 1, nir_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            nir_tuple = struct.unpack('f' * nir_band.XSize, nir_scanline)

            # Loop through the columns within the image
            for i in range(len(red_tuple)):
                # Calculate the NDVI for the current pixel.
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi = 0
                # Be careful of zero divide
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    ndvi = ndvi_upper / ndvi_lower
                print(ndvi)

    # The function from which the script runs.
    def run(self):
        # Define the input and output images
        filePathNIR = "data-test/0015/IMG_180621_094108_0000_NIR.TIF"
        filePathRED = "data-test/0015/IMG_180621_094108_0000_REG.TIF"

        outFilePath = " data-test/NDVI.tif"
        # Check the input file exists
        if os.path.exists(filePathNIR) and os.path.exists(filePathRED):
            # Run calcNDVI function
            self.calcNDVI(filePathNIR, filePathRED, outFilePath)
        else:
            print('The file does not exist.')


# Start the script by calling the run function.
if __name__ == '__main__':
    obj = GDALCalcNDVI()
    obj.run()


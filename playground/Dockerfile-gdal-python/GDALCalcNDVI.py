#! /usr/bin/env python

# Import required libraries from python
import sys, os, struct
import osgeo.gdal as gdal
from numpy import interp


# Define the class GDALCalcNDVI
class GDALCalcNDVI (object):

    # A function to create the output image
    # @staticmethod
    # A function to create the output image
    def create_output_image(self, out_file_path, in_data_set):
        # Define the image driver to be used
        # This defines the output file format (e.g., GeoTiff)
        driver = gdal.GetDriverByName("GTiff")
        # Check that this driver can create a new file.
        metadata = driver.GetMetadata()
        print(metadata)
        if gdal.DCAP_CREATE in metadata and metadata[gdal.DCAP_CREATE] == 'YES':
            print('Driver GTiff supports Create() method.')
        else:
            print('Driver GTIFF does not support Create()')
            sys.exit(-1)
        # Get the spatial information from the input file
        # geoTransform = in_data_set.GetGeoTransform()
        # geoProjection = in_data_set.GetProjection()
        # Create an output file of the same size as the inputted
        # image, but with only 1 output image band.
        new_data_set = driver.Create(out_file_path, in_data_set.RasterXSize, in_data_set.RasterYSize, 1, gdal.GDT_Float32)
        # Define the spatial information for the new image.
        # newDataset.SetGeoTransform(geoTransform)
        # newDataset.SetProjection(geoProjection)
        return new_data_set

    # The function which loops through the input image and
    # calculates the output NDVI value to be outputted.
    # @staticmethod
    def ndvi_calculator(self, file_path_nir, file_path_red, out_file_path):
        # Open the inputted data set
        data_set_nir = gdal.Open(file_path_nir, gdal.GA_ReadOnly)
        data_set_red = gdal.Open(file_path_red, gdal.GA_ReadOnly)

        # Check the dataset was successfully opened
        if data_set_nir  is None:
            print("The data set could not opened, data set NIR")
            sys.exit(-1)
        if data_set_red is None:
            print("The data set could not opened, data set RED")
            sys.exit(-1)

        # Create the output data set
        out_data_set = self.create_output_image(out_file_path, data_set_red)
        # Check the data sets was successfully created.
        if out_data_set is None:
            print('Could not create output image')
            sys.exit(-1)

        # Get hold of the RED and NIR image bands from the image
        # Note that the image bands have been hard coded
        # in this case for the Landsat sensor. RED = 3
        # and NIR = 4 this might need to be changed if
        # data from another sensor was used.
        red_band = data_set_nir.GetRasterBand(1)  # RED BAND
        nir_band = data_set_red.GetRasterBand(1)  # NIR BAND
        # Retrieve the number of lines within the image
        num_lines = red_band.YSize
        # Loop through each line in turn.
        for line in range(num_lines):
            # Define variable for output line.
            output_line = ''
            # Read in data for the current line from the
            # image band representing the red wavelength
            red_scan_line = red_band.ReadRaster(0, line, red_band.XSize, 1, red_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            red_tuple = struct.unpack('f' * red_band.XSize, red_scan_line)

            # Read in data for the current line from the
            # image band representing the NIR wavelength
            nir_scan_line = nir_band.ReadRaster(0, line, nir_band.XSize, 1, nir_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            nir_tuple = struct.unpack('f' * nir_band.XSize, nir_scan_line)

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
                ndvi = ndvi_upper / ndvi_lower
                # Add the current pixel to the output line
                output_line = output_line + struct.pack('f', ndvi).decode('UTF-8', 'ignore')
                # Write the completed line to the output image
                out_data_set.GetRasterBand(1).WriteRaster(0, line, red_band.XSize, 1, output_line, buf_xsize=red_band.XSize, buf_ysize=1, buf_type=gdal.GDT_Float32)
            # Delete the output line following write
            del output_line
        print('NDVI Calculated and Outputted to File')

    # The function from which the script runs.
    def run(self):
        # Define the input and output images
        file_path_nir = "data-test/0015/IMG_180621_094108_0000_NIR.TIF"
        file_path_red = "data-test/0015/IMG_180621_094108_0000_REG.TIF"
        out_file_path = "data-test/NDVI.TIF"

        # Check the input file exists
        if os.path.exists(file_path_nir) and os.path.exists(file_path_red):
            # Run calcNDVI function
            self.ndvi_calculator(file_path_nir, file_path_red, out_file_path)
        else:
            print('The file does not exist.')


# Start the script by calling the run function.
if __name__ == '__main__':
    obj = GDALCalcNDVI()
    obj.run()

# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import imutils
import numpy as np
import cv2


class ImageUtils:
    clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(9, 9))  # PT_5
    # clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(15, 15))  # PT_6
    thermals_datetime = {}

    def __init__(self, path):
        print(">>> INITIATING IMAGE: {}".format(path[1]))
        self.root_path = path[0]
        self.file_name = path[1]
        self.file_datetime = self.extract_datetime(self.file_name)
        print(">\t[-] Date/Time extracted.")
        self.closest_image = self.match_thermal()
        (self.minY, self.minX), (self.maxY, self.maxX), self.collage, self.filter = self.match_images()
        print("=" * 60)

    @classmethod
    def import_thermal_images(cls, path, typeof='.tiff'):
        print(">>> Importing thermal Images . . .")
        print(path)
        for root, subs, files in os.walk(path):
            print(len(files))
            for file in files:
                if not file.endswith(typeof):
                    print("\t\t[*] {} is not a valid name.".format(file))
                    continue
                cls.thermals_datetime[(root, file)] = cls.extract_datetime(file)
        if len(cls.thermals_datetime) < 1:
            raise Exception('Thermal Images not found! Please check the directory.')

    @staticmethod
    def show(*args, terminate=False, time=0):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        channels = np.concatenate([arg for arg in args], axis=1)
        cv2.imshow('image', channels)
        cv2.waitKey(time)
        if terminate:
            cv2.destroyAllWindows()

    @staticmethod
    def extract_datetime(file):
        sync_time = timedelta(hours=1, minutes=59, seconds=24)  # For PT_8.
        # sync_time = timedelta(hours=1, minutes=59, seconds=31)  # For PT_10.
        # sync_time = timedelta(hours=1, minutes=59, seconds=26)  # For PT_5.
        # sync_time = timedelta(hours=1, minutes=59, seconds=10)  # For PT_6.
        # sync_time = timedelta(hours=1, minutes=59, seconds=26)  # For PT_9.
        try:
            image_date_time = datetime.strptime(file.split('.')[0][:-8], 'IMG_%y%m%d_%H%M%S_')
            return image_date_time + sync_time
        except ValueError:
            image_date_time = datetime.strptime(file.split('.')[0], '%Y%m%d_%H%M%S')
            return image_date_time
        except :
            print(">\t\t[*] {} is not a date/time format, is it?".format(file))

    @staticmethod
    def mix_channels(path):
        for root, subs, files in os.walk(path):
            for sub in subs:
                gre = np.zeros(1, 1)
                red = np.zeros(1, 1)
                nir = np.zeros(1, 1)

                for _root, _subs, _files in os.walk(os.path.join(root, sub)):
                    for file in _files:
                        if "GRE" in file:
                            gre = cv2.imread(os.path.join(_root, file), 0)
                            gre = gre.reshape(gre.shape[0], gre.shape[1], 1)

                        if "NIR" in file:
                            nir = cv2.imread(os.path.join(_root, file), 0)
                            nir = nir.reshape(nir.shape[0], nir.shape[1], 1)

                        if "RED" in file:
                            red = cv2.imread(os.path.join(_root, file), 0)
                            red = red.reshape(red.shape[0], red.shape[1], 1)

                    # if not gre == None and not nir == None and not red == None:
                    arr_mix_channels = np.append(np.append(red, nir, 2), gre, 2)
                    cv2.imshow("mix", arr_mix_channels)
                    cv2.waitKey()

    def match_thermal(self):
        closest_image = sorted(list(self.thermals_datetime.keys())[:],
                               key=lambda x: abs(self.file_datetime - self.thermals_datetime[x]))[0]

        time_span = abs(self.file_datetime - self.thermals_datetime[closest_image])

        if time_span < timedelta(seconds=2):
            print(">\t\tRGB image: {}\n>\t\tThermal image: {}\n>\t[-] Time span: {}".format(self.file_name,
                                                                                            closest_image[1],
                                                                                            time_span))
            return closest_image, time_span
        else:
            print(">\t[*] No Match Found!")

    # def copyXMP(self, target_file):
    #     xmp_file_original = XMPFiles(file_path=self.file_name, open_forupdate=True)
    #     xmp_original = xmp_file_original.get_xmp()
    #
    #     xmp_crop_file = XMPFiles(file_path=target_file, open_forupdate=True)
    #     assert xmp_crop_file.can_put_xmp(xmp_original), "Houston, we have a problem!"
    #
    #     xmp_crop_file.put_xmp(xmp_original)
    #     xmp_crop_file.close_file()
    #     print("\tXMP Updated!")

    def match_images(self):
        # ## RGB pre-processing
        rgb_image = cv2.imread(os.path.join(self.root_path, self.file_name), 1)

        if not self.closest_image:
            print(">\t[*] No Thermal to Match.")
            collage = np.zeros(rgb_image.shape)
            overlap = np.zeros(rgb_image.shape)
            return (None, None), (None, None), collage, overlap

        rgb_image_main = imutils.rotate_bound(rgb_image, 0)
        rgb_image_main_ax0 = rgb_image_main.shape[0]
        rgb_image_main_ax1 = rgb_image_main.shape[0]

        # offset_0 = int(rgb_image_main.shape[0] / 10)  # PT_6
        # offset_1 = int(rgb_image_main.shape[1] / 10)  # PT_6

        offset_0 = int(rgb_image_main.shape[0] / 3.5)  # PT_5
        offset_1 = int(rgb_image_main.shape[1] / 5)  # PT_5

        rgb_image = rgb_image_main[offset_0:rgb_image_main_ax0 - offset_0, offset_1:rgb_image_main_ax1 - offset_1, :]
        # rgb_image = self.__class__.clahe.apply(rgb_image)
        blur_rgb = cv2.GaussianBlur(rgb_image, (11, 11), 10)
        # rgb_edges = cv2.Canny(blur_rgb, 90, 100)
        bins = np.linspace(0, 255, num=3)
        bins_index = np.digitize(blur_rgb, bins).astype(np.float64) / 3
        bins_index_1 = cv2.Canny((bins_index[:, :, 0] * 255).astype(np.uint8), 190, 210)
        bins_index_2 = cv2.Canny((bins_index[:, :, 1] * 255).astype(np.uint8), 190, 210)
        bins_index_3 = cv2.Canny((bins_index[:, :, 2] * 255).astype(np.uint8), 190, 210)
        rgb_edges = cv2.bitwise_or(bins_index_1, bins_index_2, bins_index_3)

        # rgb_edges = cv2.dilate(rgb_edges, np.ones((3, 3)), iterations=3)
        # rgb_edges = cv2.erode(rgb_edges, np.ones((3, 3)), iterations=3)

        # rgb_edges = cv2.resize(rgb_edges, None, fx=.2, fy=.2)
        rgb_edges = cv2.blur(rgb_edges, (5, 5))  # PT_6

        # ## Template pre-processing
        template = cv2.imread(os.path.join(self.closest_image[0][0], self.closest_image[0][1]),  -1).astype('uint8')
        template = imutils.rotate_bound(template, 180)
        template = cv2.resize(template, (1728, 1217), interpolation=cv2.INTER_CUBIC)
        blur_template = cv2.GaussianBlur(template, (7, 7), 7)
        equ_template = self.__class__.clahe.apply(blur_template)
        template_edges = cv2.Canny(equ_template, 30, 50)

        # template_edges = cv2.dilate(template_edges, np.ones((3, 3)), iterations=3)
        # template_edges = cv2.erode(template_edges, np.ones((3, 3)), iterations=3)

        # template_edges = cv2.resize(template_edges, None, fx=.2, fy=.2)
        template_edges = cv2.blur(template_edges, (5, 5))  # PT_6

        h, w = template.shape

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                   'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[0])  # PT_5
        # method = eval(methods[1])  # PT_6
        res = cv2.matchTemplate(rgb_edges, template_edges, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc  # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum

        top_left = (top_left[0] + offset_1, top_left[1] + offset_0)
        bottom_right = (top_left[0] + w, top_left[1] + h)

        print(">\t[-] Thermal placed @ {} of the RGB".format(top_left))

        overlap = np.zeros((rgb_image_main.shape[0], rgb_image_main.shape[1], 3)).astype(np.uint8)
        cv2.rectangle(overlap, top_left, bottom_right, color=(0, 0, 255), thickness=-1)
        overlap[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0], 1] = template
        overlap[:, :, 0] = cv2.cvtColor(rgb_image_main, cv2.COLOR_BGR2GRAY)
        # self.show(overlap, time=2)

        # collage = cv2.cvtColor(rgb_image_main, cv2.COLOR_BGR2GRAY)
        # cv2.rectangle(collage,
        #               (offset_1, offset_0),
        #               (rgb_image_main.shape[1] - offset_1,
        #                rgb_image_main.shape[0] - offset_0),
        #               color=0,
        #               thickness=9)
        #
        #  top_left[0]:bottom_right[0]] = equ_template
        # self.show(collage, time=2)
        collage = None

        return top_left, bottom_right, collage, overlap


# if __name__ == '__main__':
#     rgb_path = "/Volumes//N__1TB/bcn-mapping/PT-8-RGB-S-01/2-DENSE CLOUD/undistortion/pmvs/images"
#     thermal_path = "/Volumes//N_1TB/agisoft-data/PT_8/FLIR/"

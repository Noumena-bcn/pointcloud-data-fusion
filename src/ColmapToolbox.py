# -*- coding: utf-8 -*-
import cv2
# noinspection PyPackageRequirements
from multiprocessing import Pool, cpu_count, current_process
from src.PointcloudFusion import ImageUtils
import os


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(counter=0)
def mi(path):
    print("\n====Task#==[{:04}]=[{}]========================"
          .format(mi.counter, current_process().name))
    mi.counter += 1
    return ImageUtils(path)


def main(rgbs_path, thermals_path, mt_act=True):
    ImageUtils.import_thermal_images(thermals_path)

    for root, subs, files in os.walk(rgbs_path):
        paths = [(root, file) for file in files if file.endswith('.JPG')]
        print(">>> CPU cores available: %d" % cpu_count())

        # if you want to use multiprocessing than True, else False
        if mt_act == True:
            with Pool(cpu_count() - 1) as pool:
                print("~~~~ Into the pool ~~~~~~~~~~~~~~~~~~~~~~~~")
                imgLst = pool.map(mi, paths[:])
                print("And OUT!")

        else:
            imgLst = map(mi, paths[:])

        print("Done Processing!")

        # create a dictionary
        imgs = {imgUtl.file_name: imgUtl for imgUtl in imgLst}

        if not os.path.exists(os.path.join(os.path.dirname(rgbs_path[:-1]), "Filters")):
            os.makedirs(
                os.path.join(os.path.dirname(rgbs_path[:-1]), "Filters")
            )
        print("Saving filters to:\n\t{}"
              .format(os.path.join(os.path.dirname(rgbs_path[:-1]), "Filters")))

        # Visualize the collages
        win = cv2.namedWindow("Good?")
        for i in imgs.values():
            if not hasattr(i, 'filter'):
                continue
            # cv2.imshow(win, i.filter)
            cv2.imwrite(
                os.path.join(os.path.dirname(
                    rgbs_path[:-1]),
                    "Filters",
                    i.file),
                i.filter)
            # cv2.imshow(win, i.collage)
            # cv2.waitKey(1)

    assert imgs
    return imgs


if __name__ == '__main__':
    rgb_path = "/Volumes//Extreme SSD/bcn-mapping/PT-8-RGB-S-01/2-DENSE CLOUD/undistortion/pmvs/images"
    trm_path = "/Volumes//Extreme SSD/agisoft-data/PT_8/_FLIR/"

    main(rgb_path, trm_path, False)

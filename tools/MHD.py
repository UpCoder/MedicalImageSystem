from SimpleITK import SimpleITK as itk
import numpy as np
import copy
from PIL import Image
class MHD:
    @staticmethod
    def read_single_file(path):
        header = itk.ReadImage(path)
        image = itk.GetArrayFromImage(header)
        image = np.array(image)
        return image
    @staticmethod
    def rescale(image):
        ww = 55
        wc = 250
        ww = max(1, ww)
        lut_min = 0
        lut_max = 255
        lut_range = np.float64(lut_max) - lut_min
        minval = ww-wc/2
        maxval = ww+wc/2
        image[image < minval] = minval
        image[image > maxval] = maxval
        to_scale = (minval < image) & (image < maxval)
        image = ((1.0*(image - minval))/(1.0*(maxval-minval))) * (lut_range*1.0) + lut_min
        image = image.astype(np.uint8)
        return image.tolist()
    @staticmethod
    def write_single_file(path, image):
        print path
        print type(path)
        print np.shape(image)
        header = itk.GetImageFromArray(image)
        itk.WriteImage(header, path)


if __name__ == '__main__':
    mhd = MHD()
    mhd.read_single_file('/study/AutoSegement/App/upload/admin/15442_2737174_2_0_4/unzip/15442_2737174_2_0_4/ART_Image.mhd')
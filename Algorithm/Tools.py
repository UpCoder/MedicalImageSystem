# -*- coding: utf-8 -*-
import SimpleITK as itk
import numpy as np
import os


class Tools:
    def __init__(self):
        print 'init Tools'

    def get_label(self, cur_number):
        if cur_number in range(0, 19) or cur_number in range(100, 120):
            return 1
        if cur_number in range(19, 29) or cur_number in range(120, 132):
            return 2
        if cur_number in range(29, 39) or cur_number in range(132, 152):
            return 3
        if cur_number in range(39, 49) or cur_number in range(152, 172):
            return 4
        if cur_number in range(49, 59) or cur_number in range(172, 185):
            return 5

    def read_mhd(self, file_name):
        header = itk.ReadImage(file_name)
        image = itk.GetArrayFromImage(header)
        return image

    def write_mhd(self, image, file_name):
        self.not_exists_create(file_name)
        header = itk.GetImageFromArray(image)
        itk.WriteImage(header, file_name)

    def find_centroid3D(self, image, flag):
        [x, y, z] = np.where(image == flag)
        centroid_x = int(np.mean(x))
        centroid_y = int(np.mean(y))
        centroid_z = int(np.mean(z))
        return centroid_x, centroid_y, centroid_z

    def not_exists_create(self, path):
        str_arr = path.split('\\')
        cur_path = str_arr[0 ]
        index = 1
        while index < len(str_arr):
            if not os.path.exists(cur_path):
                print 'mkdir : ', cur_path
                os.mkdir(cur_path)
            cur_path = os.path.join(cur_path, str_arr[index])
            index += 1
    dirs = [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [-1, 1, 0],
        [-1, 0, 0],
        [-1, -1, 0],
        [0, -1, 0],
        [1, -1, 0],

        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
        [-1, 1, 1],
        [-1, 0, 1],
        [-1, -1, 1],
        [0, -1, 1],
        [1, -1, 1],

        [1, 0, -1],
        [1, 1, -1],
        [0, 1, -1],
        [-1, 1, -1],
        [-1, 0, -1],
        [-1, -1, -1],
        [0, -1, -1],
        [1, -1, -1],

        [0, 0, 1],
        [0, 0, -1]
    ]

    def okxyz(self, point, size, flag=None):
        for i in range(len(point)):
            if point[i] < 0 or point[i] >= size[i]:
                return False
        if flag is not None:
            # 使用过该点了
            if flag[point] == 0:
                return False
            else:
                return True
                # flag[point] = 0
        return True

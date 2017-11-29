# -*- coding: utf-8 -*-
from Tools import Tools
import numpy as np
import math
import sys
sys.setrecursionlimit(300000000) #例如这里设置为一百万
tools = Tools()

dirs = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
    [1, -1],
    [1, 1],
    [-1, -1],
    [-1, 1]
]
class FindBorder:
    def __init__(self):
        print 'init find border'


    # 判断一个点是不是边界上的点
    @staticmethod
    def is_border(x, y, slice):
        size = 3
        if tools.okxyz([x, y], np.shape(slice)) == False:
            return False
        for dir in dirs:
            new_x = x + dir[0] * size
            new_y = y + dir[1] * size
            if slice[x, y] != 0 \
                    and ((1.0 * (slice[new_x, new_y] - slice[x, y])) / (1.0 * slice[x, y])) >= 0.7 \
                    and ((1.0 * (slice[new_x, new_y] - slice[x, y])) > 30.0) \
                    and (slice[new_x, new_y] > 0):
                return True
        return False
    # 判断一个点是不是病灶上的点
    @staticmethod
    def is_focus(x, y, slice):
        if tools.okxyz([x, y], np.shape(slice)) == False:
            return False
        threshold_low = -20
        threshold_up = 40
        average = 0.0
        for dir in dirs:
            new_x = x + dir[0]
            new_y = y + dir[1]
            average += slice[new_x, new_y]
        average += slice[x, y]
        average /= 9.0
        if threshold_low <= average <= threshold_up:
            return True
        return False

    #  画一个大圆，向内缩紧填充
    @staticmethod
    def find_border_fullcircle(mhd_image, mask_image):
        [o, m, n] = np.shape(mhd_image)
        target_z = -1
        for z in range(o):
            if np.sum(mask_image[z, :, :]) != 0:
                target_z = z
                break

        target_slice_mhd = mhd_image[target_z, :, :]
        target_slice_mask = mask_image[target_z, :, :]
        (xs, ys) = np.where(target_slice_mask == 1)
        minx = np.min(xs)
        maxx = np.max(xs)
        miny = np.min(ys)
        maxy = np.max(ys)
        for x in range(minx, maxx):
            for y in range(miny, maxy):
                if FindBorder.is_border(x, y, target_slice_mhd):
                    target_slice_mask[x, y] = 2

        mask_image[target_z, :, :] = target_slice_mask
        tools.write_mhd(mask_image, './result.mhd')

    # 根据病灶内一个点找到整个病灶
    @staticmethod
    def find_border_onepoint(mhd_image, mask_image):
        [mask_z, mask_y, mask_x] = np.where(mask_image == 1)
        mask_z = mask_z[0]
        mask_y = mask_y[0]
        mask_x = mask_x[0]
        def find_border(mhd_slice, mask_slice, x, y, usedflag):
            if FindBorder.is_focus(x, y, mhd_slice) and usedflag[x, y] == 1:
                if FindBorder.is_border(x, y, mhd_slice):
                    usedflag[x, y] = 0
                    mask_slice[x, y] = 1
                    return
                usedflag[x, y] = 0
                mask_slice[x, y] = 1
                #print x, y
                for dir in dirs:
                    new_x = x + dir[0]
                    new_y = y + dir[1]
                    find_border(mhd_slice, mask_slice, new_x, new_y, usedflag)
        [o, n, m] = np.shape(mhd_image)
        usedflag = np.ones([n,m])

        find_border(mhd_image[mask_z, :, :], mask_image[mask_z, :, :], mask_y, mask_x, usedflag)
        cur_z = mask_z -1
        while cur_z >= 0 and FindBorder.is_focus(mask_y, mask_x, mhd_image[cur_z, :, :]):
            print cur_z
            usedflag = np.ones([n, m])
            find_border(mhd_image[cur_z, :, :], mask_image[cur_z, :, :], mask_y, mask_x, usedflag)
            cur_z -= 1
        cur_z = mask_z + 1
        while cur_z < o and FindBorder.is_focus(mask_y, mask_x, mhd_image[cur_z, :, :]):
            print cur_z
            usedflag = np.ones([n, m])
            find_border(mhd_image[cur_z, :, :], mask_image[cur_z, :, :], mask_y, mask_x, usedflag)
            cur_z += 1
        tools.write_mhd(mask_image, './find_border_onepoint.mhd')
        return mask_image


if __name__ == '__main__':
    mhd_file_name = '/Users/Liang/Desktop/Liver/Srr000/MHD/Srr000_ART.mhd'
    mask_file_name = '/Users/Liang/Desktop/Liver/Srr000/AutoSegement/art.mhd'
    mhd_image = tools.read_mhd(mhd_file_name)
    mask_image = tools.read_mhd(mask_file_name)
    FindBorder.find_border_onepoint(mhd_image, mask_image)




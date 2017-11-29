# -*- coding: utf-8 -*-
import os
import zipfile
import numpy as np
import sys
from tools import MHD
reload(sys)
sys.setdefaultencoding('utf-8')
class Tools:
    @staticmethod
    def save_zipfile(file, upload_dir, user_name, file_name):
        final_path = os.path.join(upload_dir, user_name, file_name.split('.')[0], file_name)
        dir_name = os.path.join(upload_dir, user_name)
        dir_dir_name = os.path.join(upload_dir, user_name, file_name.split('.')[0])
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        if not os.path.exists(dir_dir_name):
            os.mkdir(dir_dir_name)
        if os.path.exists(final_path):
            os.remove(final_path)
        destination = open(final_path, 'wb+')
        for chunk in file.chunks():
            print 'wrinting path'
            destination.write(chunk)
        destination.close()
        return final_path

    @staticmethod
    def unzip(file_name, output_path):
        print file_name, output_path
        files = zipfile.ZipFile(file_name, 'r')
        for file in files.namelist():
            print file
            files.extract(file, output_path)
        files.close()

    @staticmethod
    def get_dir_construction_json(dir_name):
        def get_item(id, parent, text, path, opened=False, selected=False):
            return {
                'id':id,
                'parent':parent,
                'text':text,
                'data':path,
                'state':{
                    'opened':opened,
                    'selected':selected
                }
            }
        def get_items(parent, count, path):
            files = os.listdir(path)
            data = []
            for file in files:
                if os.path.isdir(os.path.join(path, file)):
                    cur_id = file + '_' + str(count)
                    data.append(get_item(
                        cur_id,
                        parent,
                        file,
                        os.path.join(path, file)
                    ))
                    count += 1
                    sub_data, count = get_items(cur_id, count, os.path.join(path, file))
                    data.extend(sub_data)
                else:
                    data.append(get_item(
                        file + '_' + str(count),
                        parent,
                        file,
                        os.path.join(path, file)
                    ))
                    count += 1
            return data, count
        dir_name = os.path.join(dir_name,'unzip')
        res = {}
        files = os.listdir(dir_name)
        data = []
        count = 0
        for file in files:
            if os.path.isdir(os.path.join(dir_name, file)):
                cur_id = file+'_'+str(count)
                data.append(get_item(
                    cur_id,
                    '#',
                    file,
                    os.path.join(dir_name, file),
                    True
                ))
                count += 1
                sub_data,count = get_items(cur_id, count, os.path.join(dir_name, file))
                data.extend(sub_data)
            else:
                data.append(get_item(
                    file + '_' + str(count),
                    '#',
                    file,
                    os.path.join(dir_name, file)
                ))
                count += 1
        res['core'] = {
            'multiple': True,
            'data':data
        }
        return res

    @staticmethod
    def str2arr(str):
        str = str[1:-1]
        splits = str.split(',')
        res = []
        for split in splits:
            res.append(split[1:-1])
        return res

    @staticmethod
    def get_image_arr(path):
        res = []
        if not os.path.isdir(path) and path.endswith('mhd'):
            res.append({
                'name':os.path.basename(path),
                'path':os.path.dirname(path),
                'image_arr':MHD.MHD.rescale(MHD.MHD.read_single_file(path))
            })
        return res

    @staticmethod
    def write_mask_image(path, indexs, shape):
        mask_image = np.zeros(shape)
        print np.shape(mask_image)
        for index in indexs:
            mask_image[index[0],index[2],index[1]] = 1
        mask_image.astype(np.int8)
        MHD.MHD.write_single_file(path, mask_image)
        return path

    @staticmethod
    def read_mask_image(path, flag=False):
        if flag:
            return MHD.MHD.rescale(MHD.MHD.read_single_file(path))
        return MHD.MHD.read_single_file(path)

    # 完成三维矩阵的转置， 第一个维度是层数
    @staticmethod
    def transpose(image):
        [o, _, _] = np.shape(image)
        for z in range(o):
            image[z, :, :] = np.transpose(image[z, :, :])
        return image

    @staticmethod
    def create_folder(base_name, folder_name):
        try:
            if os.path.exists(os.path.join(base_name, folder_name)):
                return False
            os.mkdir(os.path.join(base_name, folder_name))
            return True
        except:
            return False

    @staticmethod
    def convert23Dim(image):
        '''
        将一幅二维的图像转化为三维的 W H->[1, W, H]
        :param image: [W H]
        :return: IMAGE: [1 W H]
        '''
        image = np.array(image)
        shape = list(np.shape(image))
        if len(shape) == 2:
            image = np.expand_dims(image, axis=0)
        return image
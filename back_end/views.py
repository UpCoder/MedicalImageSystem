# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from front_end import models
from django.db.models import Q
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core import serializers
import pandas as pd
from tools import Tools
from Algorithm import FindBorder
import json
import os
import sys
from glob import glob
reload(sys)
import Cookie
sys.setdefaultencoding('utf-8')
import numpy as np
# Create your views here.
def login(request):
    print os.getcwd()
    input_name = request.POST['username']
    input_password = request.POST['password']
    findRes = models.User.objects.filter(
        Q(username=input_name) & Q(password=input_password)
    )
    if len(findRes) >= 1:
        res = {}
        res['url'] = '/webApp/'
        res['message'] = 'success'
        response = HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        response.set_cookie('username', input_name, 3600)
        response.set_cookie('is_login', True, 3600)
        return response
    else:
        res = {}
        res['url'] = '/webApp/login'
        res['message'] = 'error'
        response = HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        return response

def logout(request):
    response = HttpResponse('logout')
    response.delete_cookie('username')
    response.delete_cookie('is_login')
    return HttpResponseRedirect('/webApp/login')

def error_message():
    res = {}
    res['message'] = 'error'
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')

def success_message(res_data, cookie_info = None):
    res = {}
    res['message'] = 'success'
    res['data']=res_data
    response = HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
    if cookie_info is not None:
        for key in cookie_info:
            response.set_cookie(key, cookie_info[key], 3600)
    return response

def upload_file(request):
    if request.method == 'POST':
        try:
            print 'ok upload file'
            upload_username = request.POST['upload_username']
            check_id = request.POST['check_id']
            shared = request.POST['shared']
            user_name = request.COOKIES.get('username', None)
            print user_name
            print shared, type(shared)
            if shared == 'on':
                shared = True
            else:
                shared = False
            uploadfile = request.FILES.get('inputfile', None)
            print uploadfile
            res = {}
            file_name = Tools.Tools.save_zipfile(uploadfile, os.path.join(os.getcwd(), 'upload'), user_name, uploadfile.name)
            Tools.Tools.unzip(file_name, os.path.join(os.path.dirname(file_name), 'unzip'))
            print 'finish unzip'
            check = models.Check(
                check_id=check_id,
                upload_username=upload_username,
                shared=shared,
                save_path=os.path.dirname(file_name)
            )
            check.save()
            print 'check id is', check.id
            print 'save path is ', os.path.dirname(file_name)
            res['message'] = 'success'
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        except Exception, e:
            print e.message
            return error_message()
    else:
        return error_message()


# 获得check数据
def get_check_data(request):
    if request.method == 'POST':
        user_name = request.COOKIES.get('username', None)
        start_index = int(request.POST['start_index'])  # 开始的下标
        per_page_num = int(request.POST['per_page_num'])  # 每页数据的个数

        find_res = models.Check.objects.filter(Q(
            upload_username=user_name
        )).all()
        print find_res.count()
        p = Paginator(find_res, per_page_num)
        cur_p = p.page(start_index)
        print cur_p.object_list
        res_data = {
            'page_num': p.num_pages,
            'cur_data': serializers.serialize('json', cur_p.object_list)
        }
        return success_message(res_data)
    else:
        return error_message()

# 获得某次check的文件路径结构
def get_file_construction_json(request):
    if request.method == 'GET':
        check_pk = request.GET['check_pk']
        print check_pk
        find_res = models.Check.objects.filter(
            Q(id=check_pk)
        )
        save_path = find_res[0].save_path
        print save_path
        data = Tools.Tools.get_dir_construction_json(save_path)
        print data
        res_data = {
            'json_data':data
        }
        return success_message(res_data)
    else:
        return error_message()

def save_image_address_cookie(request):
    if request.method == 'POST':
        address = request.POST['adresses']
        return success_message({},{
            'image_addresses': address
        })
    else:
        return error_message()


def save_mask(request):
    if request.method == 'POST':
        mask_image_index = json.loads(request.POST.get('mask_image', '[]'))
        mask_image_shape = json.loads(request.POST.get('mask_shape', '[]'))
        save_path = request.POST.get('save_path', '')
        if save_path == '':
            save_path = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))[0]
        save_path = str(save_path)
        save_path = Tools.Tools.write_mask_image(save_path, mask_image_index, mask_image_shape)
        file_name = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))[0]
        path = file_name[0:file_name.find('unzip')]
        data = Tools.Tools.get_dir_construction_json(path)
        return success_message({
            'save_path':save_path,
            'json_data': data,
        })
    else:
        return error_message()


def segement_cyst(request):
    if request.method == 'POST':
        mask_image_index = json.loads(request.POST.get('mask_image', '[]'))
        main_image_path = request.POST.get('load_main_image_path', '')
        print 'main_image_path is ', main_image_path
        main_image_path = str(main_image_path)
        # path = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))[0]
        mhd_image = Tools.Tools.read_mask_image(main_image_path)
        mask_image = np.zeros(np.shape(mhd_image))
        for index in mask_image_index:
            mask_image[index[0],index[2],index[1]] = 1
        new_mask_image = FindBorder.FindBorder.find_border_onepoint(mhd_image, mask_image)
        new_mask_image = Tools.Tools.transpose(new_mask_image)  # Web 显示的时候需要转置一下
        return success_message({
            'mask_image':new_mask_image.tolist()
        })
    else:
        return error_message()

# 获取当前绘制图像的默认存储路径以及名字
def get_save_mask_path(request):
    if request.method == 'GET':
        file_name = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))[0]
        path = file_name[0:file_name.find('unzip')]
        data = Tools.Tools.get_dir_construction_json(path)
        print data
        res_data = {
            'json_data': data
        }
        return success_message(res_data)
    else:
        return error_message()

def create_new_folder(request):
    if request.method == 'POST':
        base_name = request.POST['select_dir']
        new_folder_name = request.POST['new_folder_name']
        create_res = Tools.Tools.create_folder(base_name, new_folder_name)
        if create_res:
            file_name = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))[0]
            path = file_name[0:file_name.find('unzip')]
            data = Tools.Tools.get_dir_construction_json(path)
            print data
            res_data = {
                'json_data': data
            }
            return success_message(res_data)
        else:
            return error_message()
    else:
        return error_message()

def delete_path(request):
    if request.method == 'POST':
        address = request.POST['addresses']
        address = str(address)
        file_name = Tools.Tools.str2arr(address)[0]
        os.system("rm -rf " + file_name)
        return success_message({

        })
    else:
        return error_message()

# 根据check的id删除check
def delete_check_by_pk(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        print 'pk is ', pk
        will_delete = models.Check.objects.filter(
            Q(id=pk)
        )[0]
        path = will_delete.save_path
        os.system('rm -rf ' + path)
        will_delete.delete()
        return success_message({

        })
    else:
        return error_message()

def load_mask_image(request):
    if request.method == 'POST':
        selected_file_path = request.POST.get('selected_mask_path', '')
        print selected_file_path
        selected_file_path = str(selected_file_path)
        if os.path.exists(selected_file_path) == False:
            return error_message()
        opened_mask_image = Tools.Tools.read_mask_image(selected_file_path)
        opened_mask_image = Tools.Tools.transpose(opened_mask_image)  # Web 显示的时候需要转置一下
        return success_message({
            'mask_image': opened_mask_image.tolist()
        })
    else:
        return error_message()

def load_main_image(request):
    if request.method == 'POST':
        selected_file_path = request.POST.get('selected_main_path', '')
        print selected_file_path
        selected_file_path = str(selected_file_path)
        if os.path.exists(selected_file_path) == False:
            return error_message()
        opened_mask_image = Tools.Tools.read_mask_image(selected_file_path, True)
        return success_message({
            'main_image': opened_mask_image
        })
    else:
        return error_message()

def get_main_images(request):
    if request.method == 'POST':
        addresses = json.loads(request.POST.get('data',''))['addresses']
        print 'get_main_images', addresses
        images = []
        for address in addresses:
            address = str(address)
            print address
            images.append(Tools.Tools.read_mask_image(address, True))
        return success_message({
            'main_images':images
        })
    else:
        return error_message()

def get_images_multiphase(request):
    if request.method == 'POST':
        addresses = json.loads(request.POST.get('data', ''))['addresses']
        print 'get_main_images', addresses
        paths = glob(os.path.join(addresses[0], '*_Image.mhd'))
        images = []
        for path in paths:
            path = str(path)
            image = Tools.Tools.read_mask_image(path, True)
            # image = Tools.Tools.convert23Dim(image)
            images.append(image)
        # images = images[0][0]
        print np.shape(images)
        return success_message({
            'main_images': images
        })
    else:
        return error_message()

def get_masks_multiphases(request):
    if request.method == 'POST':
        addresses = json.loads(request.POST.get('data', ''))['addresses']
        print 'get_main_images', addresses
        paths = glob(os.path.join(addresses[0], '*_Mask.mhd'))
        images = []
        for path in paths:
            path = str(path)
            print path
            image = Tools.Tools.read_mask_image(path, False)
            image = np.squeeze(image)
            image = np.transpose(image)
            image = image.tolist()
            # image = Tools.Tools.convert23Dim(image)
            images.append(image)
        # images = images[0][0]
        print np.shape(images)
        return success_message({
            'main_images': images
        })
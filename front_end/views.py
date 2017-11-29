# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from tools import Tools
import json
# Create your views here.
def login(request):
    if request.COOKIES.get('is_login', False):
        print 'has login'
        return redirect('/webApp')
    return render(request, 'login.html')

def my_render(request, params):
    return render(
        request,
        'home.html',
        params
    )
def index(request):
    print request.COOKIES.get('is_login', False)
    if request.COOKIES.get('is_login', False):
        html_name = 'managedata/managedata.html'
        return my_render(request,{
                'content':html_name,
                'tabIndex':0
            })
    else:
        return redirect('./login')

def image(request):
    if request.COOKIES.get('is_login', False):
        # 获取image address
        addresses = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))
        print addresses
        html_name = 'image/image.html'
        data = {
            'addresses':addresses
        }
        return my_render(request,{
                'content': html_name,
                'tabIndex': 0,
                'data':json.dumps(data)
            })
    else:
        return redirect('/webApp/login')

def classification(request):
    if request.COOKIES.get('is_login', False):
        # 获取图像的存储路径
        addresses = Tools.Tools.str2arr(request.COOKIES.get('image_addresses', None))
        print addresses
        html_name = 'classfication/image.html'
        data = {
            'addresses': addresses
        }
        return my_render(request, {
            'content': html_name,
            'tabIndex': 0,
            'data': json.dumps(data)
        })
    else:
        return redirect('/webApp/login')
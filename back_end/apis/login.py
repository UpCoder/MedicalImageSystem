# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from front_end import models
from django.db.models import Q
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
        return response
    else:
        res = {}
        res['url'] = '/webApp/login'
        res['message'] = 'error'
        response = HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        return response

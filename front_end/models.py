# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

# 对应一次检查
class Check(models.Model):
    check_id = models.CharField(max_length=30)  # 检查号
    shared = models.BooleanField(default=True)  # 是否共享
    upload_username = models.CharField(max_length=30, default='admin')  # 上传者的名字
    save_path = models.CharField(max_length=100)  # 存储的路径

    def __str__(self):
        return 'check_id is ',self.check_id

    def __unicode__(self):
        return '%s' % (self.shared)

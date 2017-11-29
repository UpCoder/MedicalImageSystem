# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_id', models.CharField(max_length=30)),
                ('shared', models.BooleanField(default=True)),
                ('upload_username', models.CharField(default='admin', max_length=30)),
                ('save_path', models.CharField(max_length=100)),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('super_detector', '0004_auto_20170707_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_login_timestamp',
        ),
    ]

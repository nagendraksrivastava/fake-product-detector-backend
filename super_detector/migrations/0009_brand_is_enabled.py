# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-13 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_detector', '0008_auto_20170710_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='is_enabled',
            field=models.BooleanField(default=True),
        ),
    ]

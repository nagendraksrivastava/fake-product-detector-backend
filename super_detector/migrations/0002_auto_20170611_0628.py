# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-11 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_detector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pin',
            field=models.IntegerField(null=True),
        ),
    ]

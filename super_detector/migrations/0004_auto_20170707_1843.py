# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_detector', '0003_auto_20170707_1834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='created',
            new_name='modified_timestamp',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='modified',
        ),
        migrations.AlterField(
            model_name='brand',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

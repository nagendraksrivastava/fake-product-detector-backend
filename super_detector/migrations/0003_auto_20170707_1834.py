# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 18:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('super_detector', '0002_auto_20170611_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_timestamp',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_login_timestamp',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

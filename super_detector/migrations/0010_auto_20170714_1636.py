# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_detector', '0009_brand_is_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='depricated_date',
            field=models.DateField(null=True),
        ),
    ]

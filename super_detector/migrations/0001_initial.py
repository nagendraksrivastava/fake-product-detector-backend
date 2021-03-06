# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-11 06:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500, null=True)),
                ('slogan', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255)),
                ('img_url', models.CharField(max_length=400, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FakeProductDetected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bar_code', models.CharField(max_length=255)),
                ('serial_no', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField()),
                ('doc_url', models.CharField(max_length=400, null=True)),
                ('buy_channel', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='FakeSellerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(max_length=255)),
                ('seller_address', models.CharField(max_length=500)),
                ('seller_website', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('bar_code', models.CharField(max_length=255)),
                ('serial_no', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=500, null=True)),
                ('manufacturing_date', models.DateField()),
                ('packaging_date', models.DateField()),
                ('depricated_date', models.DateField()),
                ('color', models.CharField(max_length=156, null=True)),
                ('model', models.CharField(max_length=255, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='super_detector.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_merchant', models.BooleanField(default=True)),
                ('profile_image', models.CharField(max_length=255, null=True)),
                ('gcm_id', models.CharField(max_length=255)),
                ('os_name', models.CharField(max_length=16, null=True)),
                ('brand_name', models.CharField(max_length=16, null=True)),
                ('dob', models.DateField(null=True)),
                ('created_timestamp', models.DateTimeField()),
                ('last_login_timestamp', models.DateTimeField()),
                ('delivary_address', models.CharField(max_length=512)),
                ('country', models.CharField(max_length=16, null=True)),
                ('city', models.CharField(max_length=16, null=True)),
                ('pin', models.IntegerField(max_length=16, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fakeproductdetected',
            name='fake_seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='super_detector.FakeSellerDetail'),
        ),
    ]

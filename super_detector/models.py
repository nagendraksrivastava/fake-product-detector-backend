# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, unique=True)
    is_merchant = models.BooleanField(null=False, default=True)  # is either merchant or App Developer
    profile_image = models.CharField(max_length=255, null=True)
    gcm_id = models.CharField(max_length=255, null=False)
    os_name = models.CharField(null=True, max_length=16)
    brand_name = models.CharField(null=True, max_length=16)
    dob = models.DateField(null=True)
    delivary_address = models.CharField(null=False, max_length=512)
    country = models.CharField(max_length=16, null=True)
    city = models.CharField(max_length=16, null=True)
    pin = models.IntegerField(null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return ' '.join([self.user.username, 'Merchant' if self.is_merchant else 'Normal User'])

    def user_id(self):
        return self.user.id


class Brand(models.Model):
    # This forgeign key is consider because of merchant user mapping to
    # particular brand
    user = models.ForeignKey(User, False)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=True)
    slogan = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=False)
    img_url = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s-%s-%s-%s" % (self.name, self.description, self.slogan, self.address)


class FakeSellerDetail(models.Model):
    seller_name = models.CharField(max_length=255, null=False)
    seller_address = models.CharField(max_length=500, null=False)
    seller_website = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class FakeProductDetected(models.Model):
    bar_code = models.CharField(max_length=255, null=False)
    serial_no = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    doc_url = models.CharField(max_length=400, null=True)
    buy_channel = models.CharField(max_length=16, null=False)
    fake_seller = models.ForeignKey(FakeSellerDetail, False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)
    img_url = models.CharField(max_length=500, null=True)
    is_enabled = models.BooleanField(null=False, default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    img_url = models.CharField(max_length=500, null=True)
    is_enabled = models.BooleanField(null=False, default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, null=True)
    bar_code = models.CharField(max_length=255, null=False)
    serial_no = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=500, null=True)
    manufacturing_date = models.DateField()
    packaging_date = models.DateField()
    depricated_date = models.DateField()
    color = models.CharField(max_length=156, null=True)
    model = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s-%s-%s-%s" % (self.name, self.bar_code, self.serial_no, self.brand)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#   if created:
#      Token.objects.create(user=instance)

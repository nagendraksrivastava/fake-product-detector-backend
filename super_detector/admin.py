# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_detector.models import UserProfile, Category, SubCategory, Product


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class SubcategoryAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)

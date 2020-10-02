# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
import json
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from super_detector.models import Category, SubCategory, Brand, Product
from django.views.decorators.csrf import csrf_exempt
from constants import *
from error_code import *


@csrf_exempt
def get_subcategory(request, category_id):
    if request.method != REQUEST_TYPE_GET:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    # Here we have a security flaw , we have to match token with user id,
    # for now any token is in the database will
    token_value = get_authorization_header(request)
    if Token.objects.get(key=token_value):
        subcategory_info = []
        for subcategory in SubCategory.objects.filter(category_id=category_id):
            if subcategory.is_enabled:
                subcategory_info += [{
                    "id": subcategory.id,
                    "name": subcategory.name,
                    "img_url": subcategory.img_url
                }]
        data = {
            STATUS_TXT: {CODE_TXT: SUCCESS, MESSAGE_TXT: ""},
            "subcategory": subcategory_info
        }
        return HttpResponse(json.dumps(data))
    else:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_TOKEN, MESSAGE_TXT: INVALID_TOKEN_TXT}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_categories(request):
    if request.method != REQUEST_TYPE_GET:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    # Here we have a security flaw , we have to match token with user id,
    # for now any token is in the database will
    token_value = get_authorization_header(request)
    if Token.objects.get(key=token_value):
        category_info = []
        for category in Category.objects.all():
            if category.is_enabled:
                category_info += [{
                    "id": category.id,
                    "name": category.name,
                    "img_url": category.img_url
                }]
        data = {
            STATUS_TXT: {CODE_TXT: SUCCESS, MESSAGE_TXT: "SUCCESS"},
            "category": category_info
        }
        return HttpResponse(json.dumps(data))
    else:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_TOKEN, MESSAGE_TXT: INVALID_TOKEN_TXT}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_brand(request, subcategory_id):
    if request.method != REQUEST_TYPE_GET:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    token_value = get_authorization_header(request)
    if Token.objects.get(key=token_value):
        brand_info = []
        for brand in Brand.objects.filter(sub_category_id=subcategory_id):
            if brand.is_enabled:
                brand_info += [{
                    "id": brand.id,
                    "name": brand.name,
                    "discription": brand.description,
                    "slogan": brand.slogan,
                    "address": brand.address,
                    "img_url": brand.img_url
                }]
        data = {
            STATUS_TXT: {CODE_TXT: SUCCESS, MESSAGE_TXT: ""},
            "brand": brand_info
        }
        return HttpResponse(json.dumps(data))
    else:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_TOKEN, MESSAGE_TXT: INVALID_TOKEN_TXT}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def search_product(request):
    if request.method != REQUEST_TYPE_POST:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    subcategory_id = body['subcategory_id']
    brand_id = body['brand_id']
    bar_code = body['barcode']
    # serial_no = body['serial_no']
    if Token.objects.get(key=token_value):
        product = Product.objects.filter(
            sub_category=subcategory_id,
            brand=brand_id,
            bar_code=bar_code
            # serial_no=serial_no commented serial no for as of  now
        )
        product_info = []
        if product:
            product_info = {
                STATUS_TXT: {CODE_TXT: SUCCESS, MESSAGE_TXT: ""},
                "product": PRODUCT_FOUND_IN_OUR_DATABASE,
                "product_code": 1
            }
            return HttpResponse(json.dumps(product_info))
        else:
            product_info = {
                STATUS_TXT: {CODE_TXT: SUCCESS, MESSAGE_TXT: ""},
                "product": PRODUCT_NOT_FOUND_IN_OUR_DATABASE,
                "product_code": 0
            }
            return HttpResponse(json.dumps(product_info))
    else:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_TOKEN, MESSAGE_TXT: INVALID_TOKEN_TXT}}
        return HttpResponse(json.dumps(json_result))

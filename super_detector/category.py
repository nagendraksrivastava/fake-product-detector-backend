# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
import json
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from super_detector.models import Category, SubCategory
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_categories(request):
    if request.method != 'GET':
        json_result = {"code": 204, "message": " this method is not supported "}
        return HttpResponse(json.dumps(json_result))
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
        data = {"category": category_info}
        return HttpResponse(json.dumps(data))
    else:
        json_result = {"code": 800, "message": " Not a valid user"}
        return HttpResponse(json.dumps(json_result))




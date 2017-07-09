# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from models import UserProfile
from super_detector.UserProfileSerializer import UserProfileSerializer
from super_detector.UserSerialzer import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
import json
from rest_framework.authtoken.models import Token
from django.db import IntegrityError


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class GetUserProfile(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# TODO need to apply pagination in this API
class GetUserList(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


@csrf_exempt
def get_user_profile(request):
    if request.method != 'GET':
        return HttpResponseForbidden
    token = get_authorization_header(request)
    user = Token.objects.get(key=token).user
    user_details = UserProfile.objects.get(user)
    serializer = UserProfileSerializer(user_details)
    return Response(serializer.data)


@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        json_result = {"code": 204, "message": "We are not supporting this for login, "}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    password = body['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        try:
            token = Token.objects.create(user=user)
        except IntegrityError:
            token = Token.objects.get(user=user)
        json_result = {"code": 200, "message": "successfull logged in ", "token": token.key}
        return HttpResponse(json.dumps(json_result))
    else:
        if User.objects.get_by_natural_key(email):
            json_result = {"code": 201, "message": "email and password combination is wrong "}
            return HttpResponse(json.dumps(json_result))
        else:
            json_result = {"code": 202, "message": "User does not exists"}
            return HttpResponse(json.dumps(json_result))


@csrf_exempt
def signup_user(request):
    if request.method != 'POST':
        json_result = {"code": 204, "message": "We are not supporting, fuck yourself"}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    password = body['password']
    firstname = body['fname']
    lastname = body['lname']
    try:
        user = User.objects.create_user(username=email, email=email, password=password)
    except:
        if User.objects.get_by_natural_key(email):
            failure_message = "Email already exists please use forgot password to reset your password"
            json_result = {"code": 203, "message": failure_message}
            return HttpResponse(json.dumps(json_result))
        else:
            failure_message = "Unable to register the user at this moment"
            json_result = {"code": 203, "message": failure_message}
            return HttpResponse(json.dumps(json_result))

    user.first_name = firstname
    user.last_name = lastname
    user.is_active = True
    user.save()

    # user profile section needs to create
    user_profile = UserProfile.objects.create(user=user)
    user_profile.os_name = "android"
    user_profile.save()
    login(request, user)
    token = Token.objects.create(user=user)
    json_result = {"code": 203, "message": "signup successfull ", "token": token.key}
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def logout_user(request):
    if request.method != 'GET':
        json_result = {"code": 204, "message": "We are not supporting, use get method instead"}
        return HttpResponse(json.dumps(json_result))
    logout(request)
    token_value = get_authorization_header(request)
    token = Token.objects.get(key=token_value)
    token.delete()
    json_result = {"code": 205, "message": " Successfully logged out  "}
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def reset_password(request):
    if request.method != 'POST':
        json_result = {"code": 209, "message": "We are not supporting, use get method instead"}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    user = User.objects.get_by_natural_key(email)
    if user:
        print ("user is available")
    else:
        json_result = {"code": 210, "message": "Email is not registered with us , please signup"}
        return HttpResponse(json.dumps(json_result))

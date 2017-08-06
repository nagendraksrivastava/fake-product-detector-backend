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
from super_detector.constants import *
from super_detector.error_code import *


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
    if request.method != REQUEST_TYPE_POST:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
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
        json_result = {STATUS_TXT:
            {
                CODE_TXT: SUCCESS,
                MESSAGE_TXT: SUCCESSFUll_LOGIN
            },
            TOKEN_TXT: token.key,
            USER_EMAIL: user.email,
            USER_FNAME: user.first_name,
            USER_LNAME: user.last_name

        }
        return HttpResponse(json.dumps(json_result))
    else:
        if User.objects.get_by_natural_key(email):
            json_result = {STATUS_TXT: {CODE_TXT: INVALID_CREDETIALS_TYPE, MESSAGE_TXT: INVALID_EMAIL_PASSWORD_TXT}}
            return HttpResponse(json.dumps(json_result))
        else:
            json_result = {STATUS_TXT: {CODE_TXT: USER_DOES_NOT_EXISTS, MESSAGE_TXT: USER_DOES_NOT_EXISTS}}
            return HttpResponse(json.dumps(json_result))


@csrf_exempt
def signup_user(request):
    if request.method != REQUEST_TYPE_POST:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    password = body['password']
    firstname = body['fname']
    lastname = body['lname']
    try:
        new_user = User.objects.create_user(username=email, email=email, password=password)
    except:
        if User.objects.get_by_natural_key(email):
            failure_message = EMAIL_ALREADY_EXISTS_TXT
            json_result = {STATUS_TXT: {CODE_TXT: EMAIL_ALREADY_EXISTS, MESSAGE_TXT: failure_message}}
            return HttpResponse(json.dumps(json_result))
        else:
            failure_message = UNABLE_TO_REGISTER
            json_result = {STATUS_TXT: {CODE_TXT: SERVER_ERROR, MESSAGE_TXT: failure_message}}
            return HttpResponse(json.dumps(json_result))

    new_user.first_name = firstname
    new_user.last_name = lastname
    new_user.is_active = True
    new_user.save()

    # user profile section needs to create
    user_profile = UserProfile.objects.create(user=new_user)
    user_profile.os_name = "android"
    user_profile.save()
    new_user = authenticate(username=email, password=password)
    if new_user:
        login(request, new_user)
    else:
        json_result = {STATUS_TXT: {CODE_TXT: 606, MESSAGE_TXT: "some problem occured with the process, please login "}}
        return HttpResponse(json.dumps(json_result))
    token = Token.objects.create(user=new_user)
    json_result = {STATUS_TXT:
        {
            CODE_TXT: SUCCESS,
            MESSAGE_TXT: SUCCESSFUll_SIGNUP
        },
        TOKEN_TXT: token.key,
        USER_EMAIL: new_user.email,
        USER_FNAME: new_user.first_name,
        USER_LNAME: new_user.last_name
    }
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def logout_user(request):
    if request.method != REQUEST_TYPE_GET:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    logout(request)
    token_value = get_authorization_header(request)
    token = Token.objects.get(key=token_value)
    token.delete()
    json_result = {STATUS_TXT: {CODE_TXT: SUCCESS, MESSAGE_TXT: SUCCESSFULL_LOGOUT}}
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def reset_password(request):
    if request.method != REQUEST_TYPE_POST:
        json_result = {STATUS_TXT: {CODE_TXT: INVALID_REQUEST_TYPE, MESSAGE_TXT: BAD_REQUEST_MESSAGE}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    user = User.objects.get_by_natural_key(email)
    if user:
        print ("user is available")
    else:
        json_result = {STATUS_TXT: {CODE_TXT: EMAIL_NOT_REGISTERED, MESSAGE_TXT: EMAIL_NOT_REGISTERED}}
        return HttpResponse(json.dumps(json_result))

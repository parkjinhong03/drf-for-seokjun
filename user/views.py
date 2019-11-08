import bcrypt
import jwt

from rest_framework import generics
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .exceptions import (
    IdIsOverlaped,
    IncorrectIdAndPw,
    InappropriateJwt,
    NoIncludeJwt
)
from .serializers import (
    LoginUserSerializers,
    SignupUserSerializers
)
from .services import (
    UserService,
    JWTService,
    OneWayHash
)


@csrf_exempt
@api_view(['POST'])
def signup_endpoint(request):
    """
description: This API deletes/uninstalls a device.
parameters:
  - name: name
    type: string
    required: true
    location: form
  - name: bloodgroup
    type: string
    required: true
    location: form
  - name: birthmark
    type: string
    required: true
    location: form
"""
    if request.method == 'POST':
        payload = OneWayHash.password_to_hash(request.data)

        # 400 bad request
        if not isinstance(payload, dict):
            return payload

        serializers = SignupUserSerializers(data=payload)

        if serializers.is_valid():
            payload = serializers.initial_data

            if UserService.check_overlap_id(payload):
                raise IdIsOverlaped

            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def login_endpoint(request):
    if request.method == 'POST':

        payload = request.data
        serializers = LoginUserSerializers(data=payload)

        if serializers.is_valid():
            payload = serializers.initial_data

            if UserService.check_id_and_password(payload):
                access_token = JWTService.create_jwt(payload)
                return Response({'access_token': access_token}, status=status.HTTP_200_OK)

            raise IncorrectIdAndPw

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def my_imformation(request):
    if request.method == 'GET':
        try:
            authorization = request.headers['Authorization']
            payload = JWTService.decode_jwt(authorization)
        except KeyError:
            raise NoIncludeJwt
        except jwt.exceptions.DecodeError:
            raise InappropriateJwt

        return Response(payload, status=status.HTTP_200_OK)

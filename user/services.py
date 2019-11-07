import bcrypt
import jwt
from datetime import datetime, timedelta

from .models import User
from rest_framework.response import Response
from rest_framework import status
from myapi.settings import JWT_SECRET_KEY


class UserService(object):

    # id 중복 체크 logic
    @staticmethod
    def check_overlap_id(payload):
        _userId = payload['userId']
        _userPw = payload['userPw']

        overlap_user = list(User.objects.filter(
            userId=_userId
        ))

        if not(len(overlap_user) == 0):
            return True

        return False

    # id, password 일치 확인
    @staticmethod
    def check_id_and_password(payload):
        _userId = payload['userId']
        _userPw = payload['userPw']

        filter_user = User.objects.get(
            userId=_userId
        )

        pw_compare = bcrypt.checkpw(_userPw.encode('utf-8'), filter_user.userPw.encode('utf-8'))

        return pw_compare


class OneWayHash(object):

    # 해시 값 만들기
    @staticmethod
    def password_to_hash(payload):
        try:
            _userPw = str(payload['userPw'])

            hashed = bcrypt.hashpw(_userPw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            payload['userPw'] = hashed

            return payload

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JWTService(object):

    # jwt encoding
    @staticmethod
    def create_jwt(payload):
        data = {
            'id': payload['userId'],
            'exp': datetime.utcnow() + timedelta(seconds=60*60*2)
        }
        encoded_jwt = jwt.encode(data, JWT_SECRET_KEY, algorithm='HS256')

        return encoded_jwt

    # jwt decoding
    @staticmethod
    def decode_jwt(authorization):
        payload = jwt.decode(authorization, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['id']

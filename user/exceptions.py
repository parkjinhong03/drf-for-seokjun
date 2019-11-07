from rest_framework.exceptions import APIException


# 회원가입용 아이디 중복 에러 처리
class IdIsOverlaped(APIException):
    status_code = 470
    default_detail = 'ID exists'


# 로그인용 아이디 비번 불일치 에러
class IncorrectIdAndPw(APIException):
    status_code = 471
    default_detail = 'Incorrect id and password'


# decode 실패 jwt
class InappropriateJwt(APIException):
    status_code = 422
    default_detail = "inappropriate jwt"


# jwt 포함 X
class NoIncludeJwt(APIException):
    status_code = 401
    default_detail = "no include jwt in headers"

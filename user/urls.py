from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    login_endpoint,
    signup_endpoint,
    my_imformation
)


urlpatterns = [
    path('signup/', signup_endpoint),
    path('login/', login_endpoint),
    path('', my_imformation),
]
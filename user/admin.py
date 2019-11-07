from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['userName', 'userId', 'userPw']


admin.site.register(User, UserAdmin)

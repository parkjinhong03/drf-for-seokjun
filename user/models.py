from django.db import models
from django.conf import settings


class User(models.Model):
    userId = models.CharField(max_length=20)
    userPw = models.CharField(max_length=100)
    userName = models.CharField(max_length=20, blank=True, default='DEFAULT VALUE')

    def __str__(self):
        return self.userId

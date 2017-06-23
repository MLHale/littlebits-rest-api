from __future__ import unicode_literals

from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User, Group

from django.contrib import admin
import base64

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    roles = models.CharField(max_length=200, blank=False, default="{\"admin\": false, \"researcher\": false, \"subject\": true}")
    gender = models.CharField(max_length=100, blank=False)
    age = models.IntegerField(blank=False)
    educationlevel = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=200, blank=False)
    ip = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.user.username

    class JSONAPIMeta:
        resource_name = "profiles"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

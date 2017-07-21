from __future__ import unicode_literals

from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User, Group

from django.contrib import admin
import base64

class Device(models.Model):
    owner = models.CharField(max_length=1000, blank=False)
    deviceid = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return str(self.deviceid)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('owner','deviceid')

class DeviceEvent(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='events')
    eventtype = models.CharField(max_length=1000, blank=False)
    power = models.IntegerField()
    timestamp = models.DateTimeField()
    userid = models.CharField(max_length=1000, blank=True)
    requestor = models.GenericIPAddressField(blank=False)

    def __str__(self):
        return str(self.eventtype) + str(self.device)

class DeviceEventAdmin(admin.ModelAdmin):
    list_display = ('device','eventtype', 'power', 'timestamp')

class ApiKey(models.Model):
    owner = models.CharField(max_length=1000, blank=False)
    key = models.CharField(max_length=5000, blank=False)

    def __str__(self):
        return str(self.owner) + str(self.key)

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('owner','key')

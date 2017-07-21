from django.contrib import admin

#if ENVIRONMENT == 'PROD':
#	from api.models import *
#else:
from api.models import *

# Register your models here.
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceEvent, DeviceEventAdmin)
admin.site.register(ApiKey, ApiKeyAdmin)

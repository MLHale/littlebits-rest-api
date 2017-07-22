from django.conf.urls import include, url

#Django Rest Framework
from rest_framework import routers

from api import controllers
from django.views.decorators.csrf import csrf_exempt

#REST API routes
router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^session', csrf_exempt(controllers.Session.as_view())),
    url(r'^register', csrf_exempt(controllers.Register.as_view())),
    url(r'^deviceevents', csrf_exempt(controllers.DeviceEvents.as_view())),
    url(r'^activatecloudbit', csrf_exempt(controllers.ActivateCloudbit.as_view())),
    url(r'^', include(router.urls)),
]

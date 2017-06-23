from django.conf.urls import include, url

#Django Rest Framework
from rest_framework import routers

from api import views
from django.views.decorators.csrf import csrf_exempt

#from rest_framework.urlpatterns import format_suffix_patterns

#REST API routes
router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)

#REST API
urlpatterns = [
    url(r'^session/', views.Session.as_view()),
    url(r'^register', csrf_exempt(views.Register.as_view())),
    url(r'^', include(router.urls)),

    #Django Rest Auth
    url(r'^auth/', include('rest_framework.urls')),

]

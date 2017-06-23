from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework_json_api.relations import *


#load django and webapp models
#from django.contrib.auth.models import *
from api.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups', 'password')
        #fields = ('url', 'username', 'email', 'groups', 'experiments')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

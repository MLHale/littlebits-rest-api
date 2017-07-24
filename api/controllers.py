#from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import *
from django.contrib.auth import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
#from django.shortcuts import render_to_response
from django.template import RequestContext
from django_filters.rest_framework import DjangoFilterBackend


from django.shortcuts import *

# Import models
from django.db import models
from django.contrib.auth.models import *
from api.models import *

#REST API
from rest_framework import viewsets, filters, parsers, renderers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from rest_framework.decorators import *
from rest_framework.authentication import *

#filters
#from filters.mixins import *

from api.pagination import *
import json, datetime, pytz
from django.core import serializers
import requests


def home(request):
   """
   Send requests to / to the ember.js clientside app
   """
   return render_to_response('ember/index.html',
               {}, RequestContext(request))

def css_example(request):
  """
  Send requests to css-example/ to the insecure client app
  """
  return render_to_response('dumb-test-app/index.html',
              {}, RequestContext(request))

class Register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username') #you need to apply validators to these
        print username
        password = request.POST.get('password') #you need to apply validators to these
        email = request.POST.get('email') #you need to apply validators to these
        gender = request.POST.get('gender') #you need to apply validators to these
        age = request.POST.get('age') #you need to apply validators to these
        educationlevel = request.POST.get('educationlevel') #you need to apply validators to these
        city = request.POST.get('city') #you need to apply validators to these
        state = request.POST.get('state') #you need to apply validators to these

        print request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'username': 'Username is taken.', 'status': 'error'})
        elif User.objects.filter(email=email).exists():
            return Response({'email': 'Email is taken.', 'status': 'error'})

        #especially before you pass them in here
        newuser = User.objects.create_user(email=email, username=username, password=password)
        newprofile = Profile(user=newuser, gender=gender, age=age, educationlevel=educationlevel, city=city, state=state)
        newprofile.save()

        return Response({'status': 'success', 'userid': newuser.id, 'profile': newprofile.id})

class Session(APIView):
    permission_classes = (AllowAny,)
    def form_response(self, isauthenticated, userid, username, error=""):
        data = {
            'isauthenticated': isauthenticated,
            'userid': userid,
            'username': username
        }
        if error:
            data['message'] = error

        return Response(data)

    def get(self, request, *args, **kwargs):
        # Get the current user
        if request.user.is_authenticated():
            return self.form_response(True, request.user.id, request.user.username)
        return self.form_response(False, None, None)

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return self.form_response(True, user.id, user.username)
            return self.form_response(False, None, None, "Account is suspended")
        return self.form_response(False, None, None, "Invalid username or password")

    def delete(self, request, *args, **kwargs):
        # Logout
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeviceEvents(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

    def post(self, request, *args, **kwargs):
        json_req = json.loads(request.POST.get('request'))

        eventtype = json_req.get('payload').get('delta')
        power = json_req.get('payload').get('percent')
        timestamp = json_req.get('timestamp')
        userid = json_req.get('user_id')
        requestor = request.META['REMOTE_ADDR']

        try:
            device = Device.objects.get(deviceid=json_req.get('bit_id'))
        except Device.DoesNotExist:
            #device not created - Create it
            device = Device(
                deviceid=json_req.get('bit_id'),
                owner=userid
            )
            device.save()

        newEvent = DeviceEvent(
            device=device,
            eventtype=eventtype,
            power=power,
            timestamp=datetime.datetime.fromtimestamp(timestamp/1000, pytz.utc),
            userid=userid,
            requestor=requestor
        )

        try:
            newEvent.clean_fields()
        except ValidationError as e:
            print e
            return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

        newEvent.save()
        print 'New Event Logged from: ' + json_req.get('bit_id')
        print json_req.get('payload')
        return Response({'success': True}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        events = DeviceEvent.objects.all()
        json_data = serializers.serialize('json', events)
        content = {'deviceevents': json_data}
        return HttpResponse(json_data, content_type='json')

class ActivateCloudbit(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

    def post(self,request):
        print 'REQUEST DATA'
        print str(request.data)

        eventtype = request.data.get('eventtype')
        timestamp = int(request.data.get('timestamp'))
        requestor = request.META['REMOTE_ADDR']
        api_key = ApiKey.objects.all().first()

        #get device info from Littlebits API
        r = requests.get('https://api-http.littlebitscloud.cc/v2/devices/', headers= {
            'Authorization' : 'Bearer ' + api_key.key
        })
        print 'Retrieving List of Devices from Littlebits:'
        print r.json()
        userid = r.json()[0].get('user_id')
        deviceid= r.json()[0].get('id')

        try:
            device = Device.objects.get(deviceid=deviceid)
        except Device.DoesNotExist:
            #device not created - Create it
            device = Device(
                deviceid=deviceid,
                owner=userid
            )
            device.save()

        print "Creating New event"

        newEvent = DeviceEvent(
            device=device,
            eventtype=eventtype,
            power=-1,
            timestamp=datetime.datetime.fromtimestamp(timestamp/1000, pytz.utc),
            userid=userid,
            requestor=requestor
        )

        print newEvent
        print "Sending Device Event to: " + str(deviceid)

        #send the new event (to turn on the device) to littlebits API
        event_req = requests.post('https://api-http.littlebitscloud.cc/v2/devices/'+deviceid+'/output', headers= {
            'Authorization' : 'Bearer ' + api_key.key
        })
        print event_req.json()

        #check to ensure the device was on and received the event
        if (event_req.json().get('success')!='true'):
            return Response({'success':False, 'error':event_req.json().get('message')}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        #check that the event is safe to store in the databse
        try:
            newEvent.clean_fields()
        except ValidationError as e:
            print e
            return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

        #log the event in the DB
        newEvent.save()
        print 'New Event Logged'
        return Response({'success': True}, status=status.HTTP_200_OK)

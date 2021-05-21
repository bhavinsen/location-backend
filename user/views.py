from django.db.models.query import RawQuerySet
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated  # <-- Here
from .serializers import LoginSerializer, RegistraionSerializer, UserSerializer, MessageSerializer
from rest_framework.decorators import api_view
from .models import User, Message
from django.db.models import Q
import jwt
from django.conf import settings
from django.core import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import requests
from math import radians, cos, sin, asin, sqrt

# from rest_framework_simplejwt.authentication import JSONWebAuthentication


# Create your views here.
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


@api_view(['POST', ])
def registration_view(request):
    if request.method == "POST":
        serializers = RegistraionSerializer(data=request.data)
        data = {}
        if serializers.is_valid():
            print("in serializers")
            account = serializers.save()
            data['response'] = "successfully user registerd"
            return Response(data, status=200)
        else:
            error = serializers.errors
            print("inelse", error)
            return JsonResponse(error, status=401)


@api_view(['POST', ])
def login_View(request):
    if request.method == "POST":
        login_ser = LoginSerializer(data=request.data)
        if login_ser.is_valid() == False:
            return Response("invalid data", status=400)
        login_data = login_ser.validated_data
        print("login_data", login_data)
        login_data['email'] = login_data['email'].lower()
        try:
            user = User.objects.get(email=login_data['email'])
            print("user", user)
        except:
            return Response({"error": "Email or password is incorrect"}, status=401)

        if not user.check_password(login_data['password']):
            return Response({"error": "Email or password is incorrect"}, status=401)
        payload = {"email": user.email,
                   "password": request.data.get('password')}
        print("payload", payload)
        jwt_token = requests.post(
            "http://127.0.0.1:8000/api/token/", payload)

        return Response({"succes": "User Successfully Login", "token": jwt_token.json().get("access", None)}, status=200)


class UserList(generics.ListAPIView):
    def get(self, request):
        queryset = User.objects.filter(~Q(is_admin=True))
        serializer_class = UserSerializer(queryset, many=True)
        return Response(serializer_class.data)


class MessagePost(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        print(data)
        print(request.user)
        message = Message(message=request.data.get("message"), latitude=request.data.get(
            "latitude"), longitude=request.data.get("longitude"), user=request.user)
        message.save()
        return Response({"success": "Successfully Save Mark"}, status=200)


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


def haversine(lon1, lat1, lon2, lat2):
    radius = 0.1
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 0.1  # Radius of earth in kilometers. Use 3956 for miles
    c_radius = c * r

    if c_radius <= radius:
        return True
    return False


class GetMessageView(APIView):
    def get(self,request):
        if request.method == "GET":
            queryset = Message.objects.all()
            m_serializer = MessageSerializer(queryset, many=True)
            message_data_in_redius = []
            center_point = [
                {'lat': float(request.user.latitude), 'lng': float(request.user.longitude)}]
            for info in m_serializer.data:

                test_point = [
                    {'lat': float(info['latitude']), 'lng': float(info["longitude"])}]

                lat1 = center_point[0]['lat']
                lon1 = center_point[0]['lng']
                lat2 = test_point[0]['lat']
                lon2 = test_point[0]['lng']

                if haversine(lon1, lat1, lon2, lat2):
                    message_data_in_redius.append(info)

            return Response(message_data_in_redius)

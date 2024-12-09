import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    response = {  "id": serializer.data['id'], 
                    "username": serializer.data['username'], 
                    "token": token.key,
                }
    return Response(response)

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data})
    return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def loggedIn(request):
    response = { True }
    return Response(response)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_missions_data(request):
    latest_url = "https://api.spacexdata.com/v5/launches/latest"
    upcoming_url = "https://api.spacexdata.com/v5/launches/upcoming"
    past_url = "https://api.spacexdata.com/v5/launches/past"

    latest_response = requests.get(latest_url)
    upcoming_response = requests.get(upcoming_url)
    past_response = requests.get(past_url)

    if latest_response.status_code == 200:
        latest_data = latest_response.json()
    else:
        latest_data = {"error": "Failed to retrieve latest launch data"}

    if upcoming_response.status_code == 200:
        upcoming_data = upcoming_response.json()[:6]  
    else:
        upcoming_data = {"error": "Failed to retrieve upcoming launches data"}

    if past_response.status_code == 200:
        past_data = past_response.json()[:6] 
    else:
        past_data = {"error": "Failed to retrieve past launches data"}

    response_data = {
        "latest": latest_data,
        "upcoming": upcoming_data,
        "past": past_data
    }

    return Response(response_data)
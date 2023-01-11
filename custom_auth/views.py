import requests

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from custom_auth.models import ExternGoogleUser
from custom_auth.serializers import RegistrationSerializer


class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        data = {'success': False}
        if user:
            login(request, user)
            data['success'] = True
        else:
            pass

        return Response(status=status.HTTP_200_OK, data=data)


class LogoutView(APIView):
    def post(self, request):
        data = {}
        logout(request)
        data['success'] = True
        return Response(status=status.HTTP_200_OK, data=data)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_creation_form = UserCreationForm(data)
        data_for_response = {}
        if user_creation_form.is_valid():
            user_creation_form.save()
            data_for_response['success'] = True
        else:
            data_for_response['success'] = False
            data_for_response['errors'] = user_creation_form.errors

        return Response(status=status.HTTP_200_OK, data=data_for_response)


class ExternAuthGoogleView(APIView):
    def get(self, request):
        params = {
            'client_id': settings.EXTERN_AUTH['google']['client_id'],
            'client_secret': settings.EXTERN_AUTH['google']['client_secret'],
            'redirect_uri': 'https://venusexperiment.ru/',
            'grant_type': 'authorization_code',
            'code': request.GET['code'],
        }
        response = requests.post('https://accounts.google.com/o/oauth2/token', params=params)
        data = response.json()
        access_token = data.get('access_token')
        if access_token:
            params = {
                'access_token': access_token,
                'id_token': data['id_token'],
                'token_type': 'Bearer',
                'expires_in': 3599,
            }
            response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', params=params)
            user_info = response.json()
            
        data_for_response = {}
        return Response(status=status.HTTP_200_OK, data=data_for_response)

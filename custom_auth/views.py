import requests

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from custom_auth.models import ExternGoogleUser, Token
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
        # Получаем токен от Google
        params = {
            'client_id': settings.EXTERN_AUTH['google']['client_id'],
            'client_secret': settings.EXTERN_AUTH['google']['client_secret'],
            'redirect_uri': '{}{}'.format(settings.SITE_URL, reverse('extern_auth_google')),
            'grant_type': 'authorization_code',
            'code': request.GET['code'],
        }
        response = requests.post('https://accounts.google.com/o/oauth2/token', params=params)
        data = response.json()
        access_token = data.get('access_token')
        if not access_token:
            context = {
                'success': False,
                'title': 'Ошибка авторизации через Google',
                'message': 'Неверный токен: {}, {}'.format(
                    data['error'],
                    data['error_description'],
                    ),
                
            }
            return render(request, 'pages/message.html', context)

        # Авторизуемся через Google, получив в ответ данные пользователя
        params = {
            'access_token': access_token,
            'id_token': data['id_token'],
            'token_type': 'Bearer',
            'expires_in': 3599,
        }
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', params=params)
        user_info = response.json()
        if not user_info['verified_email']:
            context = {'success': False, 'title': 'Ошибка авторизации через Google', 'message': 'E-mail в учётной записи Google не подтверждён. Пожалуйста, подтвердите e-mail и попробуйте авторизоваться вновь.'}
            return render(request, 'pages/message.html', context)

        user_hashed_id = user_info['id']
        temp_username = '{}-{}'.format(
            user_info['email'].split('@')[0],
            user_hashed_id[:15],
        )
        ext_user_set = ExternGoogleUser.objects.filter(extern_id=user_hashed_id)
        if not ext_user_set.count():
            # Регистрируем пользователя
            user = User(username=temp_username, email=user_info['email'])
            user.save()
            ext_user = ExternGoogleUser(user=user, extern_id=user_hashed_id, is_username_changed=False)
            ext_user.save()
        else:
            ext_user = ext_user_set.get()

        login(request, ext_user.user)
        if not ext_user.is_username_changed:
            return Response(status=status.HTTP_307_TEMPORARY_REDIRECT, headers={'location': reverse('extern_registration')})

        # Авторизуем пользователя
        context = {'success': True, 'title': 'Успешная авторизация через Google', 'message': 'Вы успешно авторизовались на сайте через Google. Теперь Вам доступны все возможности сервера'}
        return render(request, 'pages/message.html', context)


class ExternRegistrationView(APIView):
    def post(self, request):
        data = {'username': request.POST['username']}#serializer.validated_data
        user = User.objects.filter(username=data['username'])
        if user.count():
            context = {'error': 'Пользователь с таким username уже существует. Пожалуйста, выберите другое username'}
            return render(request, 'pages/change_username_after_first_extern_auth.html', context=context)

        request.user.username = data['username']
        request.user.save()
        ext_user = ExternGoogleUser.objects.filter(user=request.user).get()
        ext_user.is_username_changed = True
        ext_user.save()
        context = {'success': True, 'title': 'Успешная авторизация через Google', 'message': 'Вы успешно авторизовались на сайте через Google. Теперь Вам доступны все возможности сервера'}
        return render(request, 'pages/message.html', context=context)

    def get(self, request):
        context = {'error': ''}
        return render(request, 'pages/change_username_after_first_extern_auth.html', context=context)


class TokenView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        tokens = Token.objects.filter(user=request.user).values()
        context = {'tokens': list(tokens)}
        return render(request, 'pages/tokens.html', context=context)

from django.urls import path

from custom_auth.views import (
    ExternAuthGoogleView,
    ExternRegistrationView,
    LoginView,
    LogoutView,
    TokenView,
    RegistrationView,
)

urlpatterns = [
    path('login', LoginView.as_view(), name='custom_login'),
    path('logout', LogoutView.as_view(), name='custom_logout'),
    path('registrate', RegistrationView.as_view(), name='custom_registration'),
    path('extern_google', ExternAuthGoogleView.as_view(), name='extern_auth_google'),
    path('extern_registrate', ExternRegistrationView.as_view(), name='extern_registration'),
    path('tokens', TokenView.as_view(), name='custom_token'),
]

from django.conf.urls import url
from django.urls import path

from custom_auth.views import (
    AddTokenView,
    DeleteTokenView,
    EditTokenView,
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
    path('token/', TokenView.as_view(), name='custom_auth_tokens'),
    path('token/add', AddTokenView.as_view(), name='custom_auth_add_token'),
    path('token/edit', EditTokenView.as_view(), name='custom_auth_edit_token'),
    url('token/delete/(?P<pk>[0-9]+)$', DeleteTokenView.as_view(), name='custom_auth_delete_token'),
]

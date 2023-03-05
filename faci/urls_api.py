from django.conf.urls import url
from django.urls import path

from faci.views import (
    AddFaciView,
    GetListFaciView,
)


urlpatterns = [
    path('add', AddFaciView.as_view(), name='faci_api_add_new'),
    path('get_list', GetListFaciView.as_view(), name='faci_api_get_list'),
]

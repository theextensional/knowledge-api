from django.urls import path

from pages.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='pages_index'),
]

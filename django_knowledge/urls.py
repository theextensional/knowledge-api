from django.contrib import admin
from django.urls import path

from django_knowledge.views import note_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/note/search/', note_search, name='api_note_search'),
]

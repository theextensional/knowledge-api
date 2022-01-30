from django.contrib import admin
from django.urls import path

from note.views import note_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/note/search/<str:query>/', note_search, name='api_note_search'),
]

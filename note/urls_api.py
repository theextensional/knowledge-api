from django.urls import path

from note.views import note_search, note_hook

urlpatterns = [
    path('search/<str:query>/', note_search, name='api_note_search'),
    path('hook/', note_hook, name='api_note_hook'),
]
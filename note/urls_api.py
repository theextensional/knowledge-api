from django.urls import path

from note.views import NoteAddView, NoteGetView, note_search, note_hook

urlpatterns = [
    path('search/<str:query>/', note_search, name='api_note_search'),
    path('get/<str:title>/', NoteGetView.as_view(), name='api_note_get'),
    path('add//', NoteAddView.as_view(), name='api_note_add'),
    path('hook/', note_hook, name='api_note_hook'),
]

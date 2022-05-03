from django.contrib import admin
from django.urls import path, include

from note.views import note_search, note_hook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/note/search/<str:query>/', note_search, name='api_note_search'),
    path('api/v1/note/hook/', note_hook, name='api_note_hook'),
    path('', include('pages.urls')),
]

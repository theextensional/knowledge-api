from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/note/', include('note.urls_api')),
    path('api/v1/faci/', include('faci.urls_api')),
    path('note/', include('note.urls')),
    path('faci/', include('faci.urls')),
    path('', include('pages.urls')),
]

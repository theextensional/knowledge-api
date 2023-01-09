from django.conf.urls import url
from django.urls import path

from faci.views import (
    FaciEditorView,
    FaciListView,
)


urlpatterns = [
    url(r'(?P<canvas_id>[0-9]+)$', FaciEditorView.as_view(), name='faci_editor'),
    path('new', FaciEditorView.as_view(), name='faci_new'),
    path('', FaciListView.as_view(), name='faci_list'),
]

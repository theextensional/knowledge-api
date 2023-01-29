from django.conf.urls import url
from django.urls import path

from faci.views import (
    FaciEditorView,
    FaciEditMembersView,
    FaciListView,
    SearchUserView,
)


urlpatterns = [
    url(r'(?P<canvas_id>[0-9]+)/member/add/$', FaciEditMembersView.as_view(), name='faci_editor_member_add'),
    url(r'(?P<canvas_id>[0-9]+)$', FaciEditorView.as_view(), name='faci_editor'),
    path('new', FaciEditorView.as_view(), name='faci_new'),
    path('search_user/', SearchUserView.as_view(), name='search_user'),
    path('', FaciListView.as_view(), name='faci_list'),
]

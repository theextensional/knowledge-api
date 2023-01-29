from django.urls import path

from note.views import (
    NoteEditorView,
    NoteListView,
)

urlpatterns = [
    #path('', NoteEditorView.as_view(), name='note_editor'),
    path('', NoteListView.as_view(), name='note_editor'),
]
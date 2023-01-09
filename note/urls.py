from django.urls import path

from note.views import (
    NoteEditorView,
)

urlpatterns = [
    path('', NoteEditorView.as_view(), name='note_editor'),
]
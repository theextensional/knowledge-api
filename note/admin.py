# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
from django.contrib import admin
from note.models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'search_title')


admin.site.register(Note, NoteAdmin)

from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    content = models.TextField(null=False)
    search_content = models.TextField(null=False)
    search_title = models.TextField(max_length=255, null=False, db_index=True)

    class Meta:
        db_table = 'app_note_note'

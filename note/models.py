from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    content = models.TextField(null=False)

    class Meta:
        db_table = 'app_note_note'

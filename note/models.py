from django.db import models

  
def prepare_to_search(value):
    return value.lower().replace('ё', 'е')


class Note(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, null=False, db_index=True, unique=True)
    content = models.TextField(verbose_name='Текст', null=False)
    search_content = models.TextField(verbose_name='Текст для поиска', null=False)
    search_title = models.TextField(verbose_name='Заголовок для поиска', max_length=255, null=False, db_index=True)

    class Meta:
        db_table = 'app_note_note'
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def fetch_search_fields(self):
        self.search_content = prepare_to_search(self.content)
        self.search_title = prepare_to_search(self.title)

# django_knowledge

"django knowledge" - это сервер базы знаний. Призван обеспечить:

- выгрузку данных из резервного хранилища в рабочее и наоборот;
- полнотекстовый поиск по хранилищу;
- добавления
- удобные API- и GUI-инструменты для управления выгрузкой, наполнения и поиска даных из различных внешних систем. Например, чат боты, приложения для веб и смартфонов.

## Запуск

Скачивание репозитория:

```sh
git clone https://github.com/TVP-Support/django_knowledge
```

Установка зависимостей:

```sh
pip install -r requirements.txt
```

Применение миграций - инициализация базы данных django-сервера. Команда применяется при инициализации и при любом изменении:

```sh
python manage.py migrate
```

Запуск сервера:

```sh
python manage.py runserver
```

Проверка доступности сервера:

<http://127.0.0.1:8000/api/v1/note/search/query/>

HTTP/2 200 возвращает JSON ответ.

## Импорт базы знаний

Загрузка данных из  репозитория в БД.

```sh
python manage.py note_load
```

| Attribute      | Type   | Required | Description                                                                                                                                                                |
| -------------- | ------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--downloader` | string | no       | способ загрузки с гитхаба. Доступные значения: `github_archive` (default) извлекает текст из архива репозитория, `github_archive` загружает каждый файл из директории `db` |
| `--uploader`   | string | no       | Место назначения сохранения данных. Доступные значения: `django_server` (default), `firestore`, `typesense`                                                                |

Пример команды:

```sh
python manage.py note_load --downloader=github_archive --uploader=django_server
```

<http://127.0.0.1:8000/api/v1/note/search/studio/>

HTTP/2 200 возвращает JSON ответ с данными заметки `studio`.

## API сервера

[Документация API](https://github.com/TVP-Support/django_knowledge/wiki)

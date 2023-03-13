import datetime
import json
import os
from urllib.parse import unquote

import requests
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status

from note.load_from_github import prepare_to_search, get_uploader, get_root_url
from note.credentials import args_uploader
from note.models import Note
from note.serializers import NoteAddViewSerializer


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def note_search(request, query):
    """Метод для поиска заметок"""
    query = unquote(query)

    search_by = request.GET.get('search-by', 'all')
    if search_by not in ('content', 'title', 'all'):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid `search-by` parameter'})

    fields = request.GET.get('fields', 'title')
    if fields not in ('content', 'title', 'all'):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid `fields` parameter'})

    operator = request.GET.get('operator', 'or')
    if operator not in ('or', 'and'):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid `operator` parameter'})

    limit = int(request.GET.get('limit', '10'))
    if not (100 >= limit > 0):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid `limit` parameter'})

    offset = int(request.GET.get('offset', '0'))
    if not (offset >= 0):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid `offset` parameter'})

    file_name = query if search_by in ('title', 'all') else None
    file_content = query if search_by in ('content', 'all') else None
    fields = ('title', 'content') if fields == 'all' else (fields,)
    uploader_name = request.GET.get('source', settings.DEFAULT_UPLOADER)
    uploader = get_uploader(uploader_name, args_uploader[uploader_name])
    data = uploader.search(
        #uploader,
        #args_uploader[uploader_name],
        operator=operator,
        limit=limit,
        offset=offset,
        fields=fields,
        file_name=file_name,
        file_content=file_content,
    )
    data['source'] = uploader_name
    data['path'] = '{}/'.format(get_root_url())
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def note_hook(request):
    """Хук для обновления заметок на сервере из принятого Pull Request'а на Github"""
    data = {'files': {}}
    action = request._request.headers.get('X-Github-Event')
    if action == 'push':
        repository = request.data.get('repository')
        repo_name = repository.get('name')
        owner_name = repository.get('owner').get('name')
        if owner_name != settings.GITHUB_OWNER or repo_name != settings.GITHUB_REPO:
            return Response(status=status.HTTP_200_OK, data={'message': 'repository or owner name has no access'})

        link = get_root_url(owner=owner_name, repo=repo_name, raw=True)
        session = requests.Session()
        prefix = settings.GITHUB_DIRECTORY
        removed = data['files'].setdefault('removed', set())
        added = data['files'].setdefault('added', set())
        modified = data['files'].setdefault('modified', set())
        for commit in request.data['commits']:
            data.setdefault('l', []).append({})
            for action_type, files in data['files'].items():
                for file in commit[action_type]:
                    if not file.startswith(prefix):
                        continue

                    data['l'][-1].setdefault(action_type, []).append(file)
                    if action_type == 'removed':
                        if file in removed:
                            removed.remove(file)

                        if file in modified:
                            modified.remove(file)

                        files.add(file)
                    elif action_type == 'modified':
                        if file not in added:
                            modified.add(file)
                    elif action_type == 'added':
                        if file in removed:
                            removed.remove(file)

                        files.add(file)

        for action_type, files in data['files'].items():
            for file in files:
                title, _ = os.path.splitext(os.path.basename(file))
                url = f'{link}/{file}'
                if action_type == 'removed':
                    Note.objects.filter(title=title).delete()
                elif action_type == 'modified':
                    request = session.get(url)
                    content = request.text
                    note = Note.objects.filter(title=title).first()
                    note.content = content
                    note.search_content = prepare_to_search(content)
                    note.save()
                elif action_type == 'added':
                    request = session.get(url)
                    content = request.text
                    note = Note(
                        title=title,
                        search_title=prepare_to_search(title),
                        content=content,
                        search_content=prepare_to_search(content),
                    )
                    note.save()

        return Response(status=status.HTTP_200_OK, data=data)


class NoteAddView(APIView):
    """Класс метода для добавления заметки"""

    def post(self, request):
        serializer = NoteAddViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uploader_name = data.get('source', settings.DEFAULT_UPLOADER)
        uploader = get_uploader(uploader_name, args_uploader[uploader_name])
        note_data = uploader.get(title=data['title'])
        if note_data:
            data = {'detail': 'Заметка с таким названием уже существует'}
            return Response(status=status.HTTP_200_OK, data=data)

        note = Note(title=data['title'], content=data['content'])
        note.fetch_search_fields()
        data = {}
        return Response(status=status.HTTP_200_OK, data=data)


class NoteGetView(APIView):
    """Класс метода для получения заметки"""

    def get(self, request, title):
        uploader_name = request.GET.get('source', settings.DEFAULT_UPLOADER)
        uploader = get_uploader(uploader_name, args_uploader[uploader_name])
        note_data = uploader.get(title=unquote(title))
        if not note_data:
            return Response(status=status.HTTP_404_NOT_FOUND)

        note_data['source'] = uploader_name
        return Response(status=status.HTTP_200_OK, data=note_data)


class NoteEditorView(APIView):
    def get(self, request):
        notes = []
        context = {'notes': notes}
        return render(request, 'pages/note_editor.html', context)


class NoteListView(View):

    def get(self, request):
        page_number = int(request.GET.get('p', '1'))

        notes = Note.objects.all()
        paginator = Paginator(notes, 20)
        page = paginator.page(page_number)
        context = {'notes': page.object_list}
        return render(request, 'pages/note_list.html', context)

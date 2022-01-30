from django.conf import settings
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from note.load_from_github import search
from note.credentials import args_uploader


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def note_search(request, query):
    search_by = request.GET.get('search-by', 'all')
    if search_by not in ('content', 'title', 'all'):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid `search-by` parameter'})

    file_name = query if search_by in ('title', 'all') else None
    file_content = query if search_by in ('content', 'all') else None
    operator = request.GET.get('operator', 'all')
    limit = int(request.GET.get('limit', '10'))
    offset = int(request.GET.get('offset', '0'))
    fields = request.GET.get('fields', 'title')
    fields = ('title', 'content') if fields == 'all' else (fields,)
    uploader = request.GET.get('source', settings.DEFAULT_UPLOADER)
    data = search(
        uploader,
        args_uploader[uploader],
        operator=operator,
        limit=limit,
        offset=offset,
        fields=fields,
        file_name=file_name,
        file_content=file_content,
    )
    return Response(status=status.HTTP_200_OK, data=data)

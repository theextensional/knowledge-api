from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from django_knowledge.utils.load_from_github import search


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def search(request):
    default_source = 'typesense'

    title = request.GET.get('title')
    content = request.GET.get('content')
    source = request.GET.get('source', default_source)
    results = search(source, args_uploader[UPLOADER], file_name=title, file_content=content)
    return Response(status=status.HTTP_200_OK, data={'success': True, 'data': results})

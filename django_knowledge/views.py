from django.conf import settings
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from django_knowledge.utils.load_from_github import search
from django_knowledge.utils.credentials import args_uploader


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def search(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    uploader = request.GET.get('source', settings.DEFAULT_UPLOADER)
    results = search(uploader, args_uploader[uploader], file_name=title, file_content=content)
    return Response(status=status.HTTP_200_OK, data={'success': True, 'data': results})

import json
import sys
from io import StringIO
from subprocess import check_output

from django.core import management
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from note.models import Note
from utils.redis import get_redis


class ServiceServerView(APIView):
    def get(self, request):
        if request.GET.get('pass') != 'shyzik93':
            return ''

        context = {
            'count_notes': Note.objects.count()
        }
        return render(request, 'pages/service_server.html', context)

    def post(self, request):
        command = request.POST.get('command')
        message = None
        if command == 'update_db':
            file_stdout = StringIO()
            sys.stderr = file_stdout
            sys.stdout = file_stdout
            management.call_command('note_load', stdout=file_stdout, stderr=file_stdout)
            message = file_stdout.getvalue()
        elif command == 'get_search_log':
            redis_instance = get_redis()
            logs = redis_instance.lrange('search_log', 0, -1)
            message = [json.loads(log) for log in logs]
        elif command == 'deploy_server':
            message = check_output('cd .. ; git pull origin main', shell=True)
        elif command == 'restart_server':
            restart_batcmd = 'touch tmp/restart.txt'
            check_output(restart_batcmd, shell=True)
        else:
            message = 'unknown command'

        data = {'message': message}
        return Response(status=status.HTTP_200_OK, data=data)


class MapInfoResourcesView(APIView):
    def get(self, request):
        filepath = 'роэ_карта_обмена_информационными_ресурсами.md'
        #with open(filepath, 'r', encoding='utf-8') as file:
        #    filecontent = file.read().encode('utf-8')

        #_, mermaid_content = filecontent.split('```mermaid\n', 1)
        context = {
            #'mermaid_content': mermaid_content.split('\n```')[0],
        }
        return render(request, 'pages/map_info_resources.html', context)


class MapMaterialResourcesView(APIView):
    def get(self, request):
        context = {}
        return render(request, 'pages/map_material_resources.html', context)


class AboutProjectView(APIView):
    def get(self, request):
        context = {}
        return render(request, 'pages/about_project.html', context)
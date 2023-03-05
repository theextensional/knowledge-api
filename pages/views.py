import json
import sys
from io import StringIO
from subprocess import check_output

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import management
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from note.models import Note
from pages.serializers import ProfileViewSerializer


class ServiceServerView(LoginRequiredMixin, APIView):
    def get(self, request):
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
        context = {
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


class ProfileView(LoginRequiredMixin, APIView):
    def get(self, request):
        context = {}
        return render(request, 'pages/profile.html', context)

    def post(self, request):
        serializer = ProfileViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=False)
        if serializer.errors:
            result_data = {'success': False, 'errors': serializer.errors}
            return Response(status=status.HTTP_200_OK, data=result_data)
        
        data = serializer.validated_data
        
        user = request.user
        update_fields = []
        if user.first_name != data['first_name']:
            user.first_name = data['first_name']
            update_fields.append('first_name')

        if user.last_name != data['last_name']:
            user.last_name = data['last_name']
            update_fields.append('last_name')

        if update_fields:
            user.save()

        result_data = {'success': True, 'updated': update_fields}
        return Response(status=status.HTTP_200_OK, data=result_data)

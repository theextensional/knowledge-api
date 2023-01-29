from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from faci.forms import (
    FaciCanvasAimForm,
    FaciCanvasMembersForm,
    FaciCanvasAgendaForm,
    FaciCanvasPreparingForm,
    FaciCanvasKeyThoughtsForm,
    FaciCanvasAgreementsForm,
)
from faci.models import FaciCanvas
from faci.serializers import (
    AddFaciViewSerializer,
    GetListFaciSerializer,
    FaciEditMembersSerializer,
)


class FaciEditorView(APIView):
    def get(self, request, canvas_id=None):
        if canvas_id:
            # Редактирование
            faci = get_object_or_404(FaciCanvas, pk=canvas_id)
            step = faci.step
            form_aim = FaciCanvasAimForm(instance=faci)
            form_members = FaciCanvasMembersForm(instance=faci)
            form_agenda = FaciCanvasAgendaForm(instance=faci)
            form_preparing = FaciCanvasPreparingForm(instance=faci)
            form_key_thoughts = FaciCanvasKeyThoughtsForm(instance=faci)
            form_agreements = FaciCanvasAgreementsForm(instance=faci)
            members = list(faci.member_set.values('invited'))
        else:
            # Создание
            if not request.user.is_authenticated:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            step = 1
            form_aim = FaciCanvasAimForm()
            form_members = FaciCanvasMembersForm()
            form_agenda = FaciCanvasAgendaForm()
            form_preparing = FaciCanvasPreparingForm()
            form_key_thoughts = FaciCanvasKeyThoughtsForm()
            form_agreements = FaciCanvasAgreementsForm()
            members = []

        context = {
            'step': step,
            'form_aim': form_aim,
            'form_members': form_members,
            'form_agenda': form_agenda,
            'form_preparing': form_preparing,
            'form_key_thoughts': form_key_thoughts,
            'form_agreements': form_agreements,
            'members': members,
        }
        return render(request, 'pages/faci_editor.html', context)

    def post(self, request, canvas_id=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        faci_form_data = request.data
        if canvas_id:
            # Редактирование
            faci = get_object_or_404(FaciCanvas, pk=canvas_id)
            if faci.user_creator != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            faci_form = FaciCanvasAimForm(faci_form_data, instance=faci)
        else:
            # Создание
            faci_form = FaciCanvasAimForm(faci_form_data)
            faci_form.instance.user_creator = request.user
            faci_form.instance.step = 2

        data_for_return = {}
        if faci_form.is_valid():
            faci_form.save()
            data_for_return['id'] = faci_form.instance.pk
        else:
            data_for_return['errors'] = faci_form.errors

        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciEditMembersView(APIView):
    def post(self, request, canvas_id, member_id=None):
        serializer = FaciEditMembersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if member_id:
            invited = User.get(username=data.invited)
            member = Member(invited=invited, for_what=data.for_what)
        else:
            pass

class FaciListView(View):
    def get(self, request):
        facis = (
            FaciCanvas.objects.order_by('-dt_create')
            .select_related('user_creator').prefetch_related('user_creator')
            .values('id', 'aim_type', 'aim', 'user_creator__username', 'dt_meeting')
        )

        aim_type_dict = dict(FaciCanvas.AIM_TYPE_CHOICES)
        for faci in facis:
            faci['aim_type'] = aim_type_dict[faci['aim_type']]

        context = {'facis': facis}
        return render(request, 'pages/faci_list.html', context)


class AddFaciView(APIView):
    AIM_TYPES = {
        'solution': FaciCanvas.AIM_TYPE_SOLUTION,
        'idea': FaciCanvas.AIM_TYPE_IDEA,
        'sync': FaciCanvas.AIM_TYPE_SYNC,
    }

    def post(self, request):
        serializer = AddFaciViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        faci = FaciCanvas(
            aim=data['aim'],
            if_not_reached=data['if_not_reached'],
            aim_type=AIM_TYPES[data['aim_type']],
        )
        faci.save()
        data_for_return = {'id': faci.id}
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class GetListFaciView(APIView):
    def get(self, request):
        serializer = GetListFaciSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        facis = (
            FaciCanvas.objects.all().order_by('-id')
            .values('id', 'aim', 'if_not_reached', 'aim_type')
        )
        facis = facis[(data['page_number']-1)*data['count_on_page']:data['count_on_page']]
        
        data_for_return = {
            'facis': facis,
            'total': FaciCanvas.objects.count(),
        }
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class SearchUserView(LoginRequiredMixin, APIView):
    def post(self, request):
        search_string = request.POST['search_string']
        usernames = User.objects.filter(username__contains=search_string).values_list('username', flat=True)[:10]
        #search_result = [{'id': username, 'value': username} for username in usernames]
        return Response(status=status.HTTP_200_OK, data=usernames)

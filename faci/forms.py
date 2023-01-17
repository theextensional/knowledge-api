from django.forms import ModelForm, DateTimeInput

from faci.models import Member, FaciCanvas


class FaciCanvasAimForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aim'].widget.attrs.update({'class': 'form-control'})
        self.fields['if_not_reached'].widget.attrs.update({'class': 'form-control'})
        self.fields['aim_type'].widget.attrs.update({'class': 'form-control'})
        # self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        # self.fields['place'].widget.attrs.update({'class': 'form-control'})
        # self.fields['key_thoughts'].widget.attrs.update({'class': 'form-control'})
        # self.fields['parked_thoughts'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = FaciCanvas
        fields = [
            'id',
            'aim',
            'if_not_reached',
            'aim_type',
            # 'dt_meeting',
            # 'duration',
            # 'place',
            # 'key_thoughts',
            # 'parked_thoughts',
        ]
        widgets = {
            'dt_meeting': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    # fields['aim'].widget.update(class_name='form-control')
    
    
class FaciCanvasMembersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = FaciCanvas
        fields = [
            'id',
        ]


class FaciCanvasAgendaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = FaciCanvas
        fields = [
            'id',
        ]


class FaciCanvasPreparingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = FaciCanvas
        fields = [
            'id',
        ]


class FaciCanvasKeyThoughtsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = FaciCanvas
        fields = [
            'id',
        ]


class FaciCanvasAgreementsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = FaciCanvas
        fields = [
            'id',
        ]


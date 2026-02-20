from django import forms
from .models import WorkDetail
from django.utils import timezone

class WorkDetailForm(forms.ModelForm):
    class Meta:
        model = WorkDetail
        fields = '__all__'
        widgets = {
            'labours': forms.CheckboxSelectMultiple(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
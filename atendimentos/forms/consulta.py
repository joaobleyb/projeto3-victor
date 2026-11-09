from django import forms

from ..models import Consulta


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'horario']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'horario': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }


class ConsultaStatusForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['status']

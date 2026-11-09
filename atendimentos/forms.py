from django import forms

from .models import Consulta, Especialidade, Medico, Paciente


class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = ['nome', 'descricao']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'especialidade', 'crm', 'telefone']


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

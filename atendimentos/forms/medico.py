from django import forms

from ..models import Medico


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'especialidade', 'crm', 'telefone']

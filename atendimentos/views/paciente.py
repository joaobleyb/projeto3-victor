from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import PacienteForm
from ..models import Paciente
from .mixins import ExclusaoProtegidaMixin, SucessoMixin


class PacienteListView(ListView):
    model = Paciente
    template_name = 'atendimentos/pacientes/lista.html'


class PacienteCreateView(SucessoMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    success_url = reverse_lazy('paciente_list')
    titulo = 'Novo paciente'


class PacienteUpdateView(SucessoMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    success_url = reverse_lazy('paciente_list')
    titulo = 'Editar paciente'


class PacienteDeleteView(ExclusaoProtegidaMixin, DeleteView):
    model = Paciente
    success_url = reverse_lazy('paciente_list')
    titulo = 'Excluir paciente'

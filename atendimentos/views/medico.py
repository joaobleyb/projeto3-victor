from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import MedicoForm
from ..models import Medico
from .mixins import ExclusaoProtegidaMixin, SucessoMixin


class MedicoListView(ListView):
    model = Medico
    template_name = 'atendimentos/medicos/lista.html'

    def get_queryset(self):
        return super().get_queryset().select_related('especialidade')


class MedicoCreateView(SucessoMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    success_url = reverse_lazy('medico_list')
    titulo = 'Novo médico'


class MedicoUpdateView(SucessoMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    success_url = reverse_lazy('medico_list')
    titulo = 'Editar médico'


class MedicoDeleteView(ExclusaoProtegidaMixin, DeleteView):
    model = Medico
    success_url = reverse_lazy('medico_list')
    titulo = 'Excluir médico'

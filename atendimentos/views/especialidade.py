from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from ..forms import EspecialidadeForm
from ..models import Especialidade
from .mixins import SucessoMixin


class EspecialidadeListView(ListView):
    model = Especialidade
    template_name = 'atendimentos/especialidades/lista.html'

    def get_queryset(self):
        return super().get_queryset().annotate(num_medicos=Count('medicos'))


class EspecialidadeCreateView(SucessoMixin, CreateView):
    model = Especialidade
    form_class = EspecialidadeForm
    success_url = reverse_lazy('especialidade_list')
    titulo = 'Nova especialidade'

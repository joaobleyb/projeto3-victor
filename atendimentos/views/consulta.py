from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ..forms import ConsultaForm, ConsultaStatusForm
from ..models import Consulta, Medico, Paciente
from .mixins import SucessoMixin


class ConsultaListView(ListView):
    model = Consulta
    template_name = 'atendimentos/consultas/lista.html'

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            'paciente', 'medico', 'medico__especialidade'
        )
        filtros = {
            'status': self.request.GET.get('status'),
            'medico_id': self.request.GET.get('medico'),
            'paciente_id': self.request.GET.get('paciente'),
            'data': self.request.GET.get('data'),
        }
        return qs.filter(**{k: v for k, v in filtros.items() if v})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Consulta.Status.choices
        context['medicos'] = Medico.objects.all()
        context['pacientes'] = Paciente.objects.all()
        return context


class ConsultaCreateView(SucessoMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    success_url = reverse_lazy('consulta_list')
    titulo = 'Agendar consulta'
    mensagem_sucesso = 'Consulta agendada com sucesso.'


class ConsultaStatusUpdateView(SucessoMixin, UpdateView):
    model = Consulta
    form_class = ConsultaStatusForm
    success_url = reverse_lazy('consulta_list')
    titulo = 'Alterar status da consulta'
    mensagem_sucesso = 'Status atualizado com sucesso.'

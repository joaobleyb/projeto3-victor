from django.contrib import messages
from django.db.models import Count, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    ConsultaForm, ConsultaStatusForm, EspecialidadeForm, MedicoForm, PacienteForm,
)
from .models import Consulta, Especialidade, Medico, Paciente


class TituloMixin:
    """Repassa um título para os templates genéricos de formulário/exclusão."""
    titulo = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['voltar_url'] = self.success_url
        return context


class SucessoMixin(TituloMixin):
    mensagem_sucesso = 'Registro salvo com sucesso.'
    template_name = 'atendimentos/form.html'

    def form_valid(self, form):
        messages.success(self.request, self.mensagem_sucesso)
        return super().form_valid(form)


class ExclusaoProtegidaMixin(TituloMixin):
    """Impede excluir registros que possuem consultas vinculadas."""
    template_name = 'atendimentos/confirmar_exclusao.html'

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                'Não é possível excluir: existem consultas vinculadas a este registro.',
            )
            return redirect(self.success_url)
        messages.success(self.request, 'Registro excluído com sucesso.')
        return response


# ---------- Especialidades ----------
class EspecialidadeListView(ListView):
    model = Especialidade
    template_name = 'atendimentos/especialidade_list.html'

    def get_queryset(self):
        return super().get_queryset().annotate(num_medicos=Count('medicos'))


class EspecialidadeCreateView(SucessoMixin, CreateView):
    model = Especialidade
    form_class = EspecialidadeForm
    success_url = reverse_lazy('especialidade_list')
    titulo = 'Nova especialidade'


# ---------- Pacientes ----------
class PacienteListView(ListView):
    model = Paciente
    template_name = 'atendimentos/paciente_list.html'


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


# ---------- Médicos ----------
class MedicoListView(ListView):
    model = Medico
    template_name = 'atendimentos/medico_list.html'

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


# ---------- Consultas ----------
class ConsultaListView(ListView):
    model = Consulta
    template_name = 'atendimentos/consulta_list.html'

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

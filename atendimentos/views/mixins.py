from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect


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
    template_name = 'atendimentos/comum/form.html'

    def form_valid(self, form):
        messages.success(self.request, self.mensagem_sucesso)
        return super().form_valid(form)


class ExclusaoProtegidaMixin(TituloMixin):
    """Impede excluir registros que possuem consultas vinculadas."""
    template_name = 'atendimentos/comum/confirmar_exclusao.html'

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

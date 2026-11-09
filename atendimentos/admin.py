from django.contrib import admin

from .models import Consulta, Especialidade, Medico, Paciente


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    search_fields = ['nome']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'data_nascimento', 'telefone']
    search_fields = ['nome', 'cpf']


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'especialidade', 'crm', 'telefone']
    list_filter = ['especialidade']
    search_fields = ['nome', 'crm']


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'paciente', 'medico', 'status']
    list_filter = ['status', 'medico', 'data']

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='consulta_list'), name='home'),

    path('especialidades/', views.EspecialidadeListView.as_view(), name='especialidade_list'),
    path('especialidades/nova/', views.EspecialidadeCreateView.as_view(), name='especialidade_create'),

    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente_delete'),

    path('medicos/', views.MedicoListView.as_view(), name='medico_list'),
    path('medicos/novo/', views.MedicoCreateView.as_view(), name='medico_create'),
    path('medicos/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='medico_update'),
    path('medicos/<int:pk>/excluir/', views.MedicoDeleteView.as_view(), name='medico_delete'),

    path('consultas/', views.ConsultaListView.as_view(), name='consulta_list'),
    path('consultas/nova/', views.ConsultaCreateView.as_view(), name='consulta_create'),
    path('consultas/<int:pk>/status/', views.ConsultaStatusUpdateView.as_view(), name='consulta_status'),
]

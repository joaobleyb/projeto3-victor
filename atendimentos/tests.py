from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .models import Consulta, Especialidade, Medico, Paciente


class ConsultaRegrasTests(TestCase):
    def setUp(self):
        esp = Especialidade.objects.create(nome='Cardiologia')
        self.medico = Medico.objects.create(nome='Dr. Ana', especialidade=esp, crm='123', telefone='1')
        self.p1 = Paciente.objects.create(nome='João', cpf='111', data_nascimento=date(1990, 1, 1), telefone='1')
        self.p2 = Paciente.objects.create(nome='Maria', cpf='222', data_nascimento=date(1985, 5, 5), telefone='2')
        self.dados = {'medico': self.medico.pk, 'data': '2026-12-01', 'horario': '10:00'}

    def agendar(self, paciente):
        return self.client.post(reverse('consulta_create'), {**self.dados, 'paciente': paciente.pk})

    def test_bloqueia_mesmo_horario_mesmo_medico(self):
        self.agendar(self.p1)
        resp = self.agendar(self.p2)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'já possui uma consulta')
        self.assertEqual(Consulta.objects.count(), 1)

    def test_permite_se_existente_cancelada(self):
        self.agendar(self.p1)
        Consulta.objects.update(status=Consulta.Status.CANCELADA)
        self.agendar(self.p2)
        self.assertEqual(Consulta.objects.count(), 2)

    def test_bloqueia_reativar_cancelada_com_conflito(self):
        self.agendar(self.p1)
        Consulta.objects.update(status=Consulta.Status.CANCELADA)
        self.agendar(self.p2)
        cancelada = Consulta.objects.get(paciente=self.p1)
        resp = self.client.post(reverse('consulta_status', args=[cancelada.pk]), {'status': 'agendada'})
        self.assertContains(resp, 'já possui uma consulta')
        cancelada.refresh_from_db()
        self.assertEqual(cancelada.status, Consulta.Status.CANCELADA)

    def test_alterar_status(self):
        self.agendar(self.p1)
        c = Consulta.objects.get()
        self.client.post(reverse('consulta_status', args=[c.pk]), {'status': 'realizada'})
        c.refresh_from_db()
        self.assertEqual(c.status, Consulta.Status.REALIZADA)

    def test_excluir_paciente_com_consulta_bloqueado(self):
        self.agendar(self.p1)
        self.client.post(reverse('paciente_delete', args=[self.p1.pk]))
        self.assertTrue(Paciente.objects.filter(pk=self.p1.pk).exists())

    def test_paginas_listagem(self):
        self.agendar(self.p1)
        for nome in ['consulta_list', 'paciente_list', 'medico_list', 'especialidade_list']:
            self.assertEqual(self.client.get(reverse(nome)).status_code, 200)
        self.assertContains(self.client.get(reverse('consulta_list')), 'Dr. Ana')

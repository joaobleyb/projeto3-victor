from django.db import models

from .especialidade import Especialidade


class Medico(models.Model):
    nome = models.CharField(max_length=150)
    especialidade = models.ForeignKey(
        Especialidade, on_delete=models.PROTECT, related_name='medicos'
    )
    crm = models.CharField('CRM', max_length=20, unique=True)
    telefone = models.CharField(max_length=20)

    class Meta:
        ordering = ['nome']
        verbose_name = 'médico'

    def __str__(self):
        return f'{self.nome} ({self.especialidade})'

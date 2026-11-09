from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    data_nascimento = models.DateField('data de nascimento')
    telefone = models.CharField(max_length=20)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

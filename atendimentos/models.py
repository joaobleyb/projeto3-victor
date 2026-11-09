from django.core.exceptions import ValidationError
from django.db import models


class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField('descrição', blank=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    data_nascimento = models.DateField('data de nascimento')
    telefone = models.CharField(max_length=20)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


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


class Consulta(models.Model):
    class Status(models.TextChoices):
        AGENDADA = 'agendada', 'Agendada'
        REALIZADA = 'realizada', 'Realizada'
        CANCELADA = 'cancelada', 'Cancelada'

    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name='consultas'
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.PROTECT, related_name='consultas',
        verbose_name='médico',
    )
    data = models.DateField()
    horario = models.TimeField('horário')
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.AGENDADA
    )

    class Meta:
        ordering = ['data', 'horario']

    def __str__(self):
        return f'{self.paciente} com {self.medico.nome} em {self.data:%d/%m/%Y} {self.horario:%H:%M}'

    def clean(self):
        # Regra: o mesmo médico não pode ter duas consultas não canceladas no mesmo horário.
        if self.status == self.Status.CANCELADA or not (
            self.medico_id and self.data and self.horario
        ):
            return
        conflito = (
            Consulta.objects.filter(
                medico_id=self.medico_id, data=self.data, horario=self.horario
            )
            .exclude(status=self.Status.CANCELADA)
            .exclude(pk=self.pk)
            .exists()
        )
        if conflito:
            raise ValidationError(
                'Este médico já possui uma consulta não cancelada nesta data e horário.'
            )

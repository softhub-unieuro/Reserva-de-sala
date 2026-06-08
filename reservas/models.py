from django.db import models
from salas.models import Curso, Turma, Sala

class Reserva(models.Model):
    criador_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        to_field='matricula',
        blank=True,
        null=True
        )
    id_curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Curso')
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    codigo_turma = models.CharField(max_length=255, verbose_name='Código da turma')
    data_inicial = models.DateField(blank=True, null=True)
    data_final = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva {self.codigo_turma} - {self.criador_por}"

class ReservaSala(models.Model):

    TURNOS = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno')
    ]

    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Reserva')
    id_sala = models.ForeignKey(Sala, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Sala')
    turno = models.CharField(max_length=15, choices=TURNOS)
    responsavel = models.CharField(max_length=255, verbose_name='Responsável')
    descricao_reserva = models.TextField(verbose_name='Descrição da reserva')
    status_reserva = models.BooleanField(default=True, verbose_name='Status da reserva')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva Sala {self.id_sala} ({self.turno})"

class HorarioOcupado(models.Model):
    
    DIAS_CHOICES = (
        (0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'),
        (3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo')
    )
    
    PERIODOS_CHOICES = (
        (1, '1º Período'),
        (2, '2º Período'),
        (3, '3º Período'),
        (4, '4º Período'),
    )
    reserva_sala = models.ForeignKey(ReservaSala, on_delete=models.CASCADE, related_name='horarios')
    
    dia_semana = models.IntegerField(choices=DIAS_CHOICES)
    periodo = models.IntegerField(choices=PERIODOS_CHOICES)
    
    class Meta:
        unique_together = ('reserva_sala', 'dia_semana', 'periodo')

    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.get_periodo_display()}"
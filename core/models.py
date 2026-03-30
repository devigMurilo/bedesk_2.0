from django.db import models
from django.contrib.auth.models import User
from datetime import time, timedelta, datetime


# Intervalos bloqueados (sem agendamento)
INTERVALOS_BLOQUEADOS = [
    (time(8, 20), time(8, 50)),    # Intervalo manhã
    (time(12, 0), time(13, 0)),    # Almoço
    (time(16, 20), time(16, 30)),  # Intervalo tarde
]

HORA_INICIO = time(7, 0)
HORA_FIM = time(18, 0)
DURACAO_SLOT_MINUTOS = 30  # cada slot tem 30 minutos


def gerar_horarios_disponiveis():
    """Gera todos os slots de horário disponíveis respeitando os intervalos."""
    horarios = []
    atual = datetime.combine(datetime.today(), HORA_INICIO)
    fim = datetime.combine(datetime.today(), HORA_FIM)

    while atual < fim:
        inicio_slot = atual.time()
        fim_slot = (atual + timedelta(minutes=DURACAO_SLOT_MINUTOS)).time()

        # Verifica se o slot cai dentro de algum intervalo bloqueado
        bloqueado = False
        for bloquear_inicio, bloquear_fim in INTERVALOS_BLOQUEADOS:
            # Slot é bloqueado se começa dentro do intervalo
            if bloquear_inicio <= inicio_slot < bloquear_fim:
                bloqueado = True
                break
            # Slot é bloqueado se o intervalo começa dentro do slot
            if inicio_slot <= bloquear_inicio < fim_slot:
                bloqueado = True
                break

        if not bloqueado and fim_slot <= HORA_FIM:
            horarios.append((inicio_slot, fim_slot))

        atual += timedelta(minutes=DURACAO_SLOT_MINUTOS)

    return horarios


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    descricao = models.TextField(blank=True, verbose_name='Descrição / Motivo')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    observacao_admin = models.TextField(blank=True, verbose_name='Observação do Administrador')

    class Meta:
        ordering = ['data', 'hora_inicio']
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} — {self.data} {self.hora_inicio:%H:%M}"

    @property
    def status_badge(self):
        cores = {
            'pendente': 'warning',
            'aceito': 'success',
            'recusado': 'danger',
            'cancelado': 'secondary',
        }
        return cores.get(self.status, 'secondary')

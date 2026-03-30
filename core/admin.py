from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data', 'hora_inicio', 'hora_fim', 'status', 'criado_em']
    list_filter = ['status', 'data']
    search_fields = ['usuario__username', 'usuario__first_name', 'descricao']
    list_editable = ['status']
    ordering = ['-data', 'hora_inicio']

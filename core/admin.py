from django.contrib import admin
from .models import Agendamento, PostagemBlog


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data', 'hora_inicio', 'hora_fim', 'status', 'criado_em']
    list_filter = ['status', 'data']
    search_fields = ['usuario__username', 'usuario__first_name', 'descricao']
    list_editable = ['status']
    ordering = ['-data', 'hora_inicio']


@admin.register(PostagemBlog)
class PostagemBlogAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'autor', 'publicado', 'destaque', 'criado_em']
    list_filter = ['publicado', 'destaque', 'categoria', 'criado_em']
    search_fields = ['titulo', 'categoria', 'resumo', 'conteudo']
    list_editable = ['publicado', 'destaque']
    prepopulated_fields = {'slug': ['titulo']}
    ordering = ['-criado_em']

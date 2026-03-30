from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
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


class PostagemBlog(models.Model):
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categoria = models.CharField(max_length=80)
    resumo = models.TextField()
    conteudo = models.TextField()
    imagem = models.URLField(blank=True, verbose_name='URL da imagem de capa')
    imagem_arquivo = models.ImageField(upload_to='blog/capas/', blank=True, verbose_name='Arquivo da imagem de capa')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='postagens_blog')
    destaque = models.BooleanField(default=False)
    publicado = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-destaque', '-criado_em']
        verbose_name = 'Postagem do blog'
        verbose_name_plural = 'Postagens do blog'

    def __str__(self):
        return self.titulo

    @property
    def autor_nome(self):
        if self.autor:
            return self.autor.get_full_name() or self.autor.username
        return 'Equipe BE-desk'

    @property
    def tempo_leitura(self):
        total_palavras = len((self.conteudo or '').split())
        minutos = max(1, round(total_palavras / 180))
        return f'{minutos} min de leitura'

    @property
    def imagem_capa(self):
        if self.imagem_arquivo:
            return self.imagem_arquivo.url
        return self.imagem

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo) or 'post-blog'
            slug = base_slug
            contador = 2
            while PostagemBlog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{contador}'
                contador += 1
            self.slug = slug

        if self.destaque:
            PostagemBlog.objects.filter(destaque=True).exclude(pk=self.pk).update(destaque=False)

        super().save(*args, **kwargs)

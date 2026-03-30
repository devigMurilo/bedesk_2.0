from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import date

from .models import Agendamento, gerar_horarios_disponiveis, INTERVALOS_BLOQUEADOS, HORA_INICIO, HORA_FIM
from .forms import AgendamentoForm, PerfilForm, RegistroForm


def is_admin(user):
    return user.is_staff


# ─── Autenticação ──────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'home'))
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {user.first_name or user.username}.')
        return redirect('home')
    return render(request, 'core/registro.html', {'form': form})


# ─── Home / Tabela de horários ─────────────────────────────────

@login_required
def home_view(request):
    hoje = date.today()
    data_selecionada = request.GET.get('data', str(hoje))
    try:
        from datetime import datetime
        data_obj = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
    except ValueError:
        data_obj = hoje

    slots = gerar_horarios_disponiveis()

    # Agendamentos do dia
    agendamentos_dia = Agendamento.objects.filter(
        data=data_obj
    ).select_related('usuario')

    # Mapa: hora_inicio -> agendamento
    mapa_agendamentos = {a.hora_inicio: a for a in agendamentos_dia}

    tabela = []
    for inicio, fim in slots:
        ag = mapa_agendamentos.get(inicio)
        tabela.append({
            'inicio': inicio,
            'fim': fim,
            'agendamento': ag,
            'livre': ag is None,
        })

    meus_agendamentos = Agendamento.objects.filter(
        usuario=request.user
    ).order_by('-data', '-hora_inicio')[:5]

    return render(request, 'core/home.html', {
        'tabela': tabela,
        'data_selecionada': data_obj,
        'hoje': hoje,
        'meus_agendamentos': meus_agendamentos,
        'intervalos': INTERVALOS_BLOQUEADOS,
        'hora_inicio': HORA_INICIO,
        'hora_fim': HORA_FIM,
    })


# ─── Agendamento ───────────────────────────────────────────────

@login_required
def novo_agendamento_view(request):
    slots = gerar_horarios_disponiveis()
    form = AgendamentoForm(request.POST or None, slots=slots)

    if request.method == 'POST' and form.is_valid():
        ag = form.save(commit=False)
        ag.usuario = request.user

        # Verifica conflito
        conflito = Agendamento.objects.filter(
            data=ag.data,
            hora_inicio=ag.hora_inicio,
            status__in=['pendente', 'aceito']
        ).exists()

        if conflito:
            messages.error(request, 'Este horário já está ocupado. Escolha outro.')
        else:
            ag.save()
            messages.success(request, 'Agendamento solicitado com sucesso! Aguarde a confirmação.')
            return redirect('meus_agendamentos')

    return render(request, 'core/novo_agendamento.html', {'form': form, 'slots': slots})


@login_required
def meus_agendamentos_view(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data', '-hora_inicio')
    return render(request, 'core/meus_agendamentos.html', {'agendamentos': agendamentos})


@login_required
def cancelar_agendamento_view(request, pk):
    ag = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    if ag.status in ('pendente', 'aceito'):
        ag.status = 'cancelado'
        ag.save()
        messages.success(request, 'Agendamento cancelado.')
    else:
        messages.error(request, 'Não é possível cancelar este agendamento.')
    return redirect('meus_agendamentos')


# ─── Perfil ────────────────────────────────────────────────────

@login_required
def perfil_view(request):
    form = PerfilForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    return render(request, 'core/perfil.html', {'form': form})


# ─── Admin ─────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_agendamentos_view(request):
    status_filtro = request.GET.get('status', 'pendente')
    agendamentos = Agendamento.objects.filter(status=status_filtro).select_related('usuario').order_by('data', 'hora_inicio')
    return render(request, 'core/admin_agendamentos.html', {
        'agendamentos': agendamentos,
        'status_filtro': status_filtro,
    })


@login_required
@user_passes_test(is_admin)
def admin_acao_view(request, pk, acao):
    ag = get_object_or_404(Agendamento, pk=pk)
    if acao == 'aceitar' and ag.status == 'pendente':
        ag.status = 'aceito'
        ag.observacao_admin = request.POST.get('observacao', '')
        ag.save()
        messages.success(request, f'Agendamento de {ag.usuario.get_full_name() or ag.usuario.username} aceito.')
    elif acao == 'recusar' and ag.status == 'pendente':
        ag.status = 'recusado'
        ag.observacao_admin = request.POST.get('observacao', '')
        ag.save()
        messages.warning(request, f'Agendamento recusado.')
    return redirect('admin_agendamentos')

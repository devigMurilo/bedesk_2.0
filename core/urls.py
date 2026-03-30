from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('agendamentos/', views.meus_agendamentos_view, name='meus_agendamentos'),
    path('agendamentos/novo/', views.novo_agendamento_view, name='novo_agendamento'),
    path('agendamentos/<int:pk>/cancelar/', views.cancelar_agendamento_view, name='cancelar_agendamento'),
    # Admin
    path('admin-painel/', views.admin_agendamentos_view, name='admin_agendamentos'),
    path('admin-painel/<int:pk>/<str:acao>/', views.admin_acao_view, name='admin_acao'),
]

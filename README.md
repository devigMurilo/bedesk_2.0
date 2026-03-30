# BE-Desk 2.0 — Sistema de Agendamento Django

## Pré-requisitos

- Python 3.10+
- pip

## Instalação


# 1. Instalar dependências
- pip install django

# 2. Criar as tabelas do banco de dados
- python manage.py migrate

# 3. Criar o superusuário (administrador)
- python manage.py createsuperuser

# 4. Iniciar o servidor
- python manage.py runserver


Acesse: http://localhost:8000

## Funcionalidades

### Usuário comum
- Cadastro e login
- Ver tabela de horários disponíveis por data
- Solicitar agendamento (fica pendente até admin confirmar)
- Cancelar agendamento pendente ou aceito
- Ver histórico de agendamentos
- Editar perfil

### Administrador 
- Tudo do usuário comum
- Painel em /admin-painel/ para aceitar/recusar pedidos
- Filtrar por status (pendente, aceito, recusado, cancelado)
- Adicionar observação ao recusar


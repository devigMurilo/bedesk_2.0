from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição / Motivo')),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('recusado', 'Recusado'), ('cancelado', 'Cancelado')], default='pendente', max_length=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('observacao_admin', models.TextField(blank=True, verbose_name='Observação do Administrador')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='auth.user')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
                'ordering': ['data', 'hora_inicio'],
            },
        ),
    ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostagemBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=180)),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('categoria', models.CharField(max_length=80)),
                ('resumo', models.TextField()),
                ('conteudo', models.TextField()),
                ('imagem', models.URLField(blank=True, verbose_name='URL da imagem de capa')),
                ('destaque', models.BooleanField(default=False)),
                ('publicado', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postagens_blog', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Postagem do blog',
                'verbose_name_plural': 'Postagens do blog',
                'ordering': ['-destaque', '-criado_em'],
            },
        ),
    ]

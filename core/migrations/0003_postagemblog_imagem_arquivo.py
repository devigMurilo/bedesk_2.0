from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_postagemblog'),
    ]

    operations = [
        migrations.AddField(
            model_name='postagemblog',
            name='imagem_arquivo',
            field=models.FileField(blank=True, upload_to='blog/capas/', verbose_name='Arquivo da imagem de capa'),
        ),
    ]

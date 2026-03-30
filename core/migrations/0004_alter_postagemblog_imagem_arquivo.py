from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_postagemblog_imagem_arquivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postagemblog',
            name='imagem_arquivo',
            field=models.ImageField(blank=True, upload_to='blog/capas/', verbose_name='Arquivo da imagem de capa'),
        ),
    ]

# Generated by Django 4.1.4 on 2023-04-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_campana_cam_link_recompensa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campana',
            name='cam_link_recompensa',
            field=models.CharField(max_length=200, null=True, verbose_name='Enlace para más información de la recompensa'),
        ),
    ]
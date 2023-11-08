# Generated by Django 4.1.4 on 2023-05-16 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0016_remove_campana_cam_fecha_posteo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_usu_cara', models.IntegerField(default=0)),
                ('per_usu_ojos', models.IntegerField(default=0)),
                ('per_usu_cejas', models.IntegerField(default=0)),
                ('per_usu_nariz', models.IntegerField(default=0)),
                ('per_usu_boca', models.IntegerField(default=0)),
                ('per_usu_orejas', models.IntegerField(default=0)),
                ('per_usu_cabello', models.IntegerField(default=0)),
                ('per_usu_vello_facial', models.IntegerField(default=0)),
                ('per_usu_lentes', models.IntegerField(default=0)),
                ('per_usu_torso', models.IntegerField(default=0)),
                ('per_usu_color_piel', models.IntegerField(default=0)),
                ('per_usu_color_torso', models.IntegerField(default=0)),
                ('per_usu_usu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.1.4 on 2023-08-14 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_int_calificar_intcal_fecha_int_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lista_Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Seleccion_Categorias_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sel_cat_cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.categoria')),
                ('sel_cat_lis_cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.lista_categorias')),
                ('sel_cat_usu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lista_categorias',
            name='categorias',
            field=models.ManyToManyField(through='app.Seleccion_Categorias_Usuario', to='app.categoria'),
        ),
    ]

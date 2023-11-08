# Generated by Django 4.1.4 on 2023-08-14 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_lista_categorias_seleccion_categorias_usuario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seleccion_categorias_usuario',
            name='sel_cat_cat_id',
        ),
        migrations.RemoveField(
            model_name='seleccion_categorias_usuario',
            name='sel_cat_lis_cat_id',
        ),
        migrations.AddField(
            model_name='seleccion_categorias_usuario',
            name='sel_cat_cat',
            field=models.ManyToManyField(to='app.categoria'),
        ),
        migrations.DeleteModel(
            name='Lista_Categorias',
        ),
    ]
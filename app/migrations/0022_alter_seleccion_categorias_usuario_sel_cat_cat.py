# Generated by Django 4.1.4 on 2023-08-15 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_seleccion_categorias_usuario_sel_cat_cat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleccion_categorias_usuario',
            name='sel_cat_cat',
            field=models.CharField(default='[]', max_length=200),
        ),
    ]

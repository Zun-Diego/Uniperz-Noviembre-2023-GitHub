# Generated by Django 4.1.4 on 2023-04-13 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_marca_mar_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='campana',
            name='cam_fecha_posteo',
            field=models.DateField(default=None, null=True),
        ),
    ]

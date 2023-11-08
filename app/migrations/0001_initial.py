# Generated by Django 4.1.4 on 2023-03-29 23:11

import birthday.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cam_nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('cam_medallas', models.IntegerField()),
                ('cam_dias', models.IntegerField()),
                ('cam_detalles', models.TextField(verbose_name='Detalles')),
                ('cam_descripcion', models.TextField(verbose_name='Descripción')),
                ('cam_fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('cam_fecha_termino', models.DateField(verbose_name='Fecha de Término')),
                ('cam_imagen', models.ImageField(upload_to='campanas', verbose_name='Imagen')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('cam_cantidad_recompensas', models.IntegerField()),
                ('cam_cantidad_recompensas_canjeadas', models.IntegerField(default=0)),
                ('cam_csv', models.FileField(null=True, upload_to='campanas', verbose_name='Archivo .csv')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cont_nombre', models.CharField(max_length=50)),
                ('cont_correo', models.EmailField(max_length=254)),
                ('cont_tipo_consulta', models.IntegerField(choices=[[0, 'consulta'], [1, 'reclamo'], [2, 'sugerencia'], [3, 'felicitaciones']])),
                ('cont_mensaje', models.TextField()),
                ('cont_avisos', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esc_numero', models.IntegerField(default=0)),
                ('esc_nombre', models.CharField(default='Sin Calificar', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option_one', models.CharField(max_length=30)),
                ('option_two', models.CharField(max_length=30)),
                ('option_three', models.CharField(max_length=30)),
                ('option_one_count', models.IntegerField(default=0)),
                ('option_two_count', models.IntegerField(default=0)),
                ('option_three_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Recomendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_nombre_desafio', models.CharField(default='Recomendar', max_length=20)),
                ('rec_booleano', models.BooleanField()),
                ('rec_dias', models.IntegerField()),
                ('rec_medallas', models.IntegerField()),
                ('rec_medallas_a_recomendar', models.IntegerField()),
                ('rec_cam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.campana')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_nombre', models.CharField(max_length=50)),
                ('pro_detalles', models.TextField()),
                ('pro_descripcion', models.TextField()),
                ('pro_imagen', models.ImageField(upload_to='productos')),
                ('pro_precio', models.IntegerField()),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('pro_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mar_imagen', models.ImageField(upload_to='marcas')),
                ('mar_nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('mar_apellido', models.CharField(default='', max_length=30)),
                ('mar_mail', models.CharField(default='', max_length=50)),
                ('mar_telefono', models.CharField(default='', max_length=30)),
                ('mar_cargo', models.CharField(default='', max_length=30)),
                ('mar_imagen_persona', models.ImageField(upload_to='marcas')),
                ('mar_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_fecha', models.DateField(default=datetime.datetime.today)),
                ('int_medallas_logradas', models.IntegerField(default=0)),
                ('int_recompensa', models.BooleanField(default=False)),
                ('int_num_recompensa', models.IntegerField(default=-1)),
                ('int_cam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.campana')),
                ('int_est_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.estado')),
                ('int_usu_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Int_Recomendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intrec_desafio', models.BooleanField(default=False)),
                ('intrec_respuesta', models.CharField(default='', max_length=200)),
                ('intrec_fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('intrec_fecha_limite', models.DateTimeField(blank=True, null=True)),
                ('intrec_int_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.interaccion')),
            ],
        ),
        migrations.CreateModel(
            name='Int_Compartir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intcom_desafio', models.BooleanField(default=False)),
                ('intcom_fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('intcom_fecha_limite', models.DateTimeField(blank=True, null=True)),
                ('intcom_int_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.interaccion')),
            ],
        ),
        migrations.CreateModel(
            name='Int_Calificar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intcal_desafio', models.BooleanField(default=False)),
                ('intcal_respuesta', models.IntegerField(choices=[[1, '1/5 - Muy Malo'], [2, '2/5 - Malo'], [3, '3/5 - Regular'], [4, '4/5 - Bueno'], [5, '5/5 - Muy Bueno']], default=0)),
                ('intcal_fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('intcal_fecha_limite', models.DateTimeField(blank=True, null=True)),
                ('intcal_int_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.interaccion')),
            ],
        ),
        migrations.CreateModel(
            name='Compartir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_nombre_desafio', models.CharField(default='Compartir', max_length=20)),
                ('com_booleano', models.BooleanField()),
                ('com_dias', models.IntegerField()),
                ('com_medallas', models.IntegerField()),
                ('com_link_ig', models.CharField(max_length=200)),
                ('com_link_tt', models.CharField(max_length=200)),
                ('com_cam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.campana')),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristicas_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_usu_alias', models.CharField(default='', max_length=30)),
                ('car_usu_fecha_nacimiento_dayofyear_internal', models.PositiveSmallIntegerField(default=None, editable=False, null=True)),
                ('car_usu_fecha_nacimiento', birthday.fields.BirthdayField()),
                ('car_usu_region', models.IntegerField(choices=[[0, 'Region de Arica y Parinacota'], [1, 'Region de Tarapacá'], [2, 'Region de Antofagasta'], [3, 'Region de Atacama'], [4, 'Region de Coquimbo'], [5, 'Region de Valparaíso'], [6, 'Region Metropolitana de Santiago'], [7, "Region del Libertador General Bernardo O'Higgins"], [8, 'Region del Maule'], [9, 'Region del Ñuble'], [10, 'Region del Biobío'], [11, 'Region de La Araucanía'], [12, 'Region de Los Ríos'], [13, 'Region de Los Lagos'], [14, 'Region de Aysén del General Carlos Ibáñez del Campo'], [15, 'Region de Magallanes y de la Antártica Chilena']], default=-1)),
                ('car_usu_color_interfaz', models.IntegerField(choices=[[0, 'Morado'], [1, 'Naranjo'], [2, 'Azul']], default=-1)),
                ('car_usu_usu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='campana',
            name='cam_categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.categoria', verbose_name='Categoría'),
        ),
        migrations.AddField(
            model_name='campana',
            name='cam_creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Calificar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cal_nombre_desafio', models.CharField(default='Calificar', max_length=20)),
                ('cal_booleano', models.BooleanField()),
                ('cal_dias', models.IntegerField()),
                ('cal_medallas', models.IntegerField()),
                ('cal_pregunta', models.CharField(max_length=200)),
                ('cal_cam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.campana')),
            ],
        ),
    ]
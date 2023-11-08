from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from Uniperz.utils import unique_slug_generator, unique_slug_generator2
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from birthday import BirthdayField, BirthdayManager
from django.forms import model_to_dict


# Create your models here.
class Categoria(models.Model):

    cat_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_nombre

class Escala(models.Model):

    esc_numero = models.IntegerField(default=0)
    esc_nombre = models.CharField(max_length=30, default='Sin Calificar')


    def __str__(self):
        return self.nombre

opciones_escala =[

    [1,"1/5 - Muy Malo"],
    [2,"2/5 - Malo"],
    [3,"3/5 - Regular"],
    [4,"4/5 - Bueno"],
    [5,"5/5 - Muy Bueno"]
]

estado_campana =[

    [0,"Default"],
    [1,"Pendiente"],
    [2,"Activa"],
    [3,"Terminada"]
]

class Campana(models.Model):

    cam_nombre = models.CharField(max_length=50, verbose_name='Nombre')

    cam_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )

    cam_medallas = models.IntegerField(default = 0)
    cam_dias = models.IntegerField(default = 0)
    cam_detalles = models.TextField(verbose_name='Detalles')
    cam_descripcion = models.TextField(verbose_name='Descripción')
    cam_fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    cam_fecha_termino = models.DateField(verbose_name='Fecha de Término')
    cam_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoría')
    cam_imagen = models.ImageField(upload_to="campanas", null=False, verbose_name='Imagen')
    slug = models.SlugField(max_length=200, null=True, blank=True)
    cam_cantidad_recompensas = models.IntegerField(null=False, default = 0)
    cam_cantidad_recompensas_canjeadas = models.IntegerField(default = 0)
    cam_csv = models.FileField (upload_to="campanas",null=True, verbose_name='Archivo .csv')
    cam_estado = models.IntegerField(choices=estado_campana,default=0)
    cam_nom_recompensa = models.CharField(max_length=50, null=False, verbose_name='Nombre Recompensa')
    cam_imagen_recompensa = models.ImageField(upload_to="campanas", null=False, verbose_name='Imagen Recompensa')
    cam_descripcion_recompensa = models.CharField(max_length = 200, null=True, verbose_name='Descripción Recompensa')
    cam_caracteristicas_recompensa = models.TextField(null=True, verbose_name='Características Recompensa')
    cam_link_recompensa = models.CharField(max_length = 200, null=True, verbose_name='Enlace para más información de la recompensa')
    
    def __str__(self):
        return self.cam_nombre

class Producto(models.Model):
    
    pro_nombre = models.CharField(max_length=50)
    pro_creador = models.ForeignKey(User, on_delete=models.CASCADE,)
    pro_detalles = models.TextField()
    pro_descripcion = models.TextField()
    pro_imagen = models.ImageField(upload_to="productos", null=False)
    pro_precio = models.IntegerField()

    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.pro_nombre

class Estado(models.Model):

    est_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.est_nombre

class Interaccion(models.Model):

    int_usu_id = models.ForeignKey(User, on_delete=models.PROTECT, )
    int_cam_id = models.ForeignKey(Campana, on_delete=models.CASCADE)
    int_est_id = models.ForeignKey(Estado,on_delete=models.PROTECT, default=1)
    int_fecha = models.DateField(default=datetime.today)
    int_medallas_logradas = models.IntegerField(default=0)

    int_recompensa = models.BooleanField(default=False)
    int_num_recompensa = models.IntegerField(default=-1)

    def __str__(self):
        return self.int_cam_id

class Calificar(models.Model):

    cal_nombre_desafio = models.CharField (max_length=20, default='Calificar')
    cal_booleano = models.BooleanField()
    cal_cam_id = models.ForeignKey(Campana, on_delete=models.CASCADE)
    cal_dias = models.IntegerField()
    cal_medallas = models.IntegerField()
    cal_pregunta = models.CharField(max_length=200)
    #calificacion = models.FloatField()

    def __str__(self):
        return self.cal_cam_id

class Int_Calificar(models.Model):

    intcal_int_id = models.ForeignKey(Interaccion, on_delete = models.CASCADE)
    intcal_desafio = models.BooleanField(default=False)
    intcal_respuesta = models.IntegerField(choices=opciones_escala,default=0)
    intcal_fecha_inicio = models.DateTimeField(null = True, blank = True)
    intcal_fecha_limite = models.DateTimeField(null = True, blank = True)
    intcal_fecha_int = models.DateTimeField(null = True, blank = True) #nuevo

    def __str__(self):
        return self.intcal_int_id

class Compartir(models.Model):

    com_nombre_desafio = models.CharField (max_length=20, default='Compartir')
    com_booleano = models.BooleanField()
    com_cam_id = models.ForeignKey(Campana, on_delete=models.CASCADE)
    com_dias = models.IntegerField()
    com_medallas = models.IntegerField()

    com_link_ig = models.CharField(max_length=200)
    com_link_tt = models.CharField(max_length=200)

    def __str__(self):
        return self.com_cam_id

class Int_Compartir(models.Model):

    intcom_int_id = models.ForeignKey(Interaccion, on_delete = models.CASCADE)
    intcom_desafio = models.BooleanField(default=False)
    intcom_fecha_inicio = models.DateTimeField(null = True, blank = True)
    intcom_fecha_limite = models.DateTimeField(null = True, blank = True)
    intcom_fecha_int = models.DateTimeField(null = True, blank = True) #nuevo

class Recomendar(models.Model):

    rec_nombre_desafio = models.CharField (max_length=20, default='Recomendar')
    rec_booleano = models.BooleanField()
    rec_cam_id = models.ForeignKey(Campana, on_delete=models.CASCADE)
    rec_dias = models.IntegerField()
    rec_medallas = models.IntegerField()
    rec_medallas_a_recomendar = models.IntegerField()

    def __str__(self):
        return self.rec_cam_id

class Int_Recomendar(models.Model):

    intrec_int_id = models.ForeignKey(Interaccion, on_delete = models.CASCADE)
    intrec_desafio = models.BooleanField(default=False)
    intrec_respuesta = models.CharField(max_length=200, default='')
    intrec_fecha_inicio = models.DateTimeField(null = True, blank = True)
    intrec_fecha_limite = models.DateTimeField(null = True, blank = True)
    intrec_fecha_int = models.DateTimeField(null = True, blank = True) #nuevo

def slug_generator(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Campana)


opciones_consultas =[
    [0,"consulta"],
    [1,"reclamo"],
    [2,"sugerencia"],
    [3,"felicitaciones"]
]



class Contacto(models.Model):

    cont_nombre = models.CharField(max_length=50)
    cont_correo = models.EmailField()
    cont_tipo_consulta = models.IntegerField(choices=opciones_consultas)
    cont_mensaje = models.TextField()
    cont_avisos = models.BooleanField()

    def __str__(self):
        return self.cont_nombre


class Poll(models.Model):

    question = models.TextField()
    #Meter array de opciones, modelar base de datos
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

opciones_regiones =[
    [0,"Region de Arica y Parinacota"],
    [1,"Region de Tarapacá"],
    [2,"Region de Antofagasta"],
    [3,"Region de Atacama"],
    [4,"Region de Coquimbo"],
    [5,"Region de Valparaíso"],
    [6,"Region Metropolitana de Santiago"],
    [7,"Region del Libertador General Bernardo O'Higgins"],
    [8,"Region del Maule"],
    [9,"Region del Ñuble"],
    [10,"Region del Biobío"],
    [11,"Region de La Araucanía"],
    [12,"Region de Los Ríos"],
    [13,"Region de Los Lagos"],
    [14,"Region de Aysén del General Carlos Ibáñez del Campo"],
    [15,"Region de Magallanes y de la Antártica Chilena"]
]

opciones_interfaz =[
    [0,"Morado"],
    [1,"Naranjo"],
    [2,"Azul"]
]


class Caracteristicas_Usuario(models.Model):

    car_usu_usu_id = models.ForeignKey(User, on_delete = models.CASCADE)
    car_usu_alias = models.CharField(max_length=30, default='')
    car_usu_fecha_nacimiento = BirthdayField()
    car_usu_region = models.IntegerField(choices=opciones_regiones,default=-1)
    car_usu_color_interfaz = models.IntegerField(choices=opciones_interfaz,default=-1)

class Seleccion_Categorias_Usuario(models.Model):

    sel_cat_usu_id = models.ForeignKey(User, on_delete = models.CASCADE)
    sel_cat_cat = models.CharField(max_length=200, default='[]')
    



class Perfil_Usuario(models.Model):

    per_usu_usu_id = models.ForeignKey(User, on_delete = models.CASCADE)
    per_usu_cara = models.IntegerField(default=0)
    per_usu_ojos = models.IntegerField(default=0)
    per_usu_cejas = models.IntegerField(default=0)
    per_usu_nariz = models.IntegerField(default=0)
    per_usu_boca = models.IntegerField(default=0)
    per_usu_orejas = models.IntegerField(default=0)
    per_usu_cabello = models.IntegerField(default=0)
    per_usu_vello_facial = models.IntegerField(default=0)
    per_usu_lentes = models.IntegerField(default=0)
    per_usu_torso = models.IntegerField(default=0)
    per_usu_color_piel = models.IntegerField(default=0)
    per_usu_color_torso = models.IntegerField(default=0)


class Marca(models.Model):

    mar_creador = models.ForeignKey(User, on_delete = models.CASCADE)
    mar_imagen = models.ImageField(upload_to="marcas", null=False, verbose_name='Logotipo Marca')
    mar_nombre = models.CharField(max_length=30, null=False,  verbose_name='Nombre')
    mar_apellido = models.CharField(max_length=30, default='', verbose_name='Apellido')
    mar_mail = models.CharField(max_length=50, default='', null=False, verbose_name='Email')
    mar_telefono = models.CharField(max_length=30, default='', null=False, verbose_name='Teléfono')
    mar_cargo = models.CharField(max_length=30, null=False, default='', verbose_name='Cargo')
    mar_imagen_persona = models.ImageField(upload_to="marcas", null=False, verbose_name='Foto Perfil')
    mar_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoría Marca', null=True)

    def __str__(self):
        return self.mar_creador.username
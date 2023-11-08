from django import forms
from django.forms import ModelForm

from .models import Calificar, Contacto, Campana, Compartir, Interaccion, Recomendar, \
    Int_Calificar, Int_Compartir, Int_Recomendar, Poll, Caracteristicas_Usuario, Marca, Producto, \
    Perfil_Usuario, Seleccion_Categorias_Usuario

from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .validators import MaxSizeFileValidator
from django.forms import ValidationError


from dobwidget import DateOfBirthWidget


class ContactoForm(forms.ModelForm):

    #nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = Contacto
        #fields = ["nombre","correo","tipo consulta","mensaje","avisos"]
        fields = '__all__'

        

class CampanaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        

    cam_nombre = forms.CharField(min_length=3, max_length=50)
    cam_imagen = forms.ImageField(required=True, validators=[MaxSizeFileValidator(max_file_size=5)])
    cam_imagen_recompensa = forms.ImageField(required=True, validators=[MaxSizeFileValidator(max_file_size=5)])
    #cam_medallas = forms.IntegerField(min_value=1,max_value=10000)
    #creador = request.user.username
    

    def clean_nombre(self):

        nombre = self.cleaned_data["cam_nombre"]
        existe = Campana.objects.filter(cam_nombre__iexact=nombre).exists()

        if existe:
            raise ValidationError("Este nombre ya existe")

        return nombre

    class Meta:

        model = Campana
        #print(model)
        fields = ["cam_nombre","cam_detalles","cam_descripcion","cam_fecha_inicio","cam_fecha_termino","cam_categoria","cam_imagen","cam_nom_recompensa","cam_imagen_recompensa","cam_descripcion_recompensa","cam_caracteristicas_recompensa","cam_link_recompensa","cam_csv"]

        widgets = {

            "cam_fecha_inicio": forms.SelectDateWidget(),
            "cam_fecha_termino": forms.SelectDateWidget(),

        }



class ProductoForm(forms.ModelForm):

    def clean_nombre(self):

        cam_nombre = self.cleaned_data["pro_nombre"]
        existe = Campana.objects.filter(pro_nombre__iexact=cam_nombre).exists()

        if existe:
            raise ValidationError("Este nombre ya existe")

        return pro_nombre

    class Meta:

        model = Producto
        print(model)
        fields = ["pro_nombre","pro_detalles", "pro_descripcion", "pro_imagen","pro_precio"]

class CalificarForm(forms.ModelForm):
    

    class Meta:

        model = Calificar
        fields = ["cal_booleano","cal_medallas","cal_dias","cal_pregunta"]

class CompartirForm(forms.ModelForm):
    
    class Meta:

        model = Compartir
        fields = ["com_booleano","com_medallas","com_dias","com_link_ig","com_link_tt"]

class Int_CalificarForm(forms.ModelForm):

    class Meta:

        model = Int_Calificar
        fields = ["intcal_respuesta"]

class RecomendarForm(forms.ModelForm):

    class Meta:
        
        model = Recomendar
        fields = ["rec_booleano","rec_dias","rec_medallas","rec_medallas_a_recomendar"]

class Int_RecomendarForm(forms.ModelForm):
    
    class Meta:

        model = Int_Recomendar
        fields = ["intrec_respuesta"]

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]


class CreatePollForm(forms.ModelForm):

    class Meta :
        model = Poll
        #Ver array de opciones
        fields = ["question" , "option_one" , "option_two" , "option_three" ] 

class CaracteristicasForm (forms.ModelForm):

    class Meta:
        model = Caracteristicas_Usuario
        fields = ["car_usu_alias", "car_usu_fecha_nacimiento", "car_usu_region", "car_usu_color_interfaz"]

        widgets = {

            "car_usu_fecha_nacimiento": DateOfBirthWidget()
        }

class MarcaForm (forms.ModelForm):

    class Meta:
        model = Marca
        fields = ["mar_nombre","mar_apellido","mar_mail","mar_telefono","mar_cargo","mar_categoria","mar_imagen","mar_imagen_persona"]

class Perfil_UsuarioForm(forms.ModelForm):

    class Meta:
        model = Perfil_Usuario
        fields = ["per_usu_cara","per_usu_cabello","per_usu_vello_facial","per_usu_torso"]

class Seleccion_Categorias_UsuarioForm(forms.ModelForm):

    class Meta:

        model = Seleccion_Categorias_Usuario
        fields = ['sel_cat_cat']


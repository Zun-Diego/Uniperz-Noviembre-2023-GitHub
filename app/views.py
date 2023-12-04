from django.shortcuts import render, redirect, get_object_or_404
from .models import Campana, Calificar, Compartir, Interaccion, Recomendar, \
    Int_Calificar, Int_Compartir, Int_Recomendar, Estado, Poll, Caracteristicas_Usuario, Marca, Producto, \
    Perfil_Usuario, Seleccion_Categorias_Usuario, Categoria

from .forms import CaracteristicasForm, CompartirForm, ContactoForm, CampanaForm, CustomUserCreationForm, \
    CalificarForm, RecomendarForm, Int_RecomendarForm, Int_CalificarForm, CreatePollForm, MarcaForm, ProductoForm, \
    Perfil_UsuarioForm, Seleccion_Categorias_UsuarioForm

from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from django.views.generic import CreateView, ListView
from datetime import datetime, timedelta, date
import csv
from Uniperz.csvlista import leer_fichero
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from Uniperz.utils import sort_third
import json
import ast

import xlwt
import sweetify


from rest_framework import viewsets
from .serializers import CampanaSerializer
from app import models

class CampanaViewset(viewsets.ModelViewSet):
    
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

def inicio(request):
    print(settings.MEDIA_ROOT)
    return render(request,'app/inicio2.html')

# Create your views here.
def home(request):

    
    color = None
    marca = None

    busqueda = request.POST.get("buscar")
    #busqueda1 = request.POST.get('buscar1', '')
    busqueda2 = request.POST.get("buscar2")
    busqueda3 = request.POST.get("buscar3")
    busqueda4 = request.POST.get("buscar4")

    #campana = Campana.objects.all()
    campana = Campana.objects.filter(Q(cam_fecha_termino__gte = date.today()) & Q(cam_fecha_inicio__lte = date.today())).order_by('-id')
    

    if busqueda:
        campana = Campana.objects.filter(
            Q(cam_nombre__icontains = busqueda) #|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
    """
    if busqueda1:
        campana = Campana.objects.filter(
            Q(cam_creador__busqueda1__icontains = busqueda1)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
    """
    if busqueda2:
        campana = Campana.objects.filter(
            Q(cam_detalles__icontains = busqueda2)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()

    if busqueda3:
        campana = Campana.objects.filter(
            Q(cam_descripcion__icontains = busqueda3)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()

    if busqueda4:
        """
        campana = Campana.objects.filter(
            Q(user__id == busqueda4)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
        """
        campana = Campana.objects.filter(Q(cam_creador__username__icontains = busqueda4))
        #DataPribadiSiswa.objects.filter(siswa_kelas__some_name__icontains=keyword2))
    
    if request.user.is_authenticated:
        grupo = request.user.groups.all()

        if grupo: 
            
            grupo = list(grupo)
            grupo = str(grupo[0])
            print(grupo)
            
            if grupo == 'Marca':
                
                marca = Marca.objects.filter(mar_creador = request.user)
                marca = marca.first()
                print("es marca")
                return redirect('listar_campanas')
            elif grupo == 'Usuario':

                caract = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id).exists()
                

                if not caract:

                    #messages.warning(request, "Debe usted ingresar sus datos")
                    
                    return redirect('caracteristicas')
                    
                else:
                    
                    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

                    if color:
                        color = color.first()
                        color = color.car_usu_color_interfaz
                    else:
                        pass
                    #print("color: ",color) #morado = 0, naranjo = 1, azul = 2
                    print("no pasa nada, todo bien")

            else:
                print("que?")

        perfil = Perfil_Usuario.objects.filter(per_usu_usu_id = request.user)
        print(perfil)
        if perfil:
            print("si hay perfil")

        else:
            print("no hay perfil")
            Perfil_Usuario.objects.create(per_usu_usu_id = request.user)

    else:
        return redirect('login')
    print("color antes del data:", color)
    data = {
        'campana' : campana,
        'marca' : marca,
        'color' : color,
    }
    
    return render(request,'app/home.html',data)

def interacciones(request):

    
    inter = Interaccion.objects.filter(int_usu_id = request.user)
    inter_list = inter.values_list('int_cam_id', flat=True)
    inter_list = list(inter_list)
    print(inter_list)

    

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    busqueda = request.POST.get("buscar")
    #busqueda1 = request.POST.get('buscar1', '')
    busqueda2 = request.POST.get("buscar2")
    busqueda3 = request.POST.get("buscar3")
    busqueda4 = request.POST.get("buscar4")

    campana = Campana.objects.filter(id__in = inter_list).order_by('-id')

    cam = campana

    print(cam)
    cam_list = cam.values_list('cam_creador', flat=True)
    print(cam_list)
    cam_list=list(cam_list)
    print("camlist: ", cam_list)
    cam_list = list(set(cam_list))
    print("cam list: ", cam_list)

    marca_list = Marca.objects.filter(mar_creador__in = cam_list).order_by('-id')
    print(marca_list)
    print("marca list:", marca_list)




    lista_de_categorias = campana.values_list('cam_categoria', flat=True)
    print(lista_de_categorias)
    lista_de_categorias = list(set(lista_de_categorias))
    print(lista_de_categorias)

    if busqueda:
        campana = Campana.objects.filter(
            Q(cam_nombre__icontains = busqueda) #|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
    """
    if busqueda1:
        campana = Campana.objects.filter(
            Q(cam_creador__busqueda1__icontains = busqueda1)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
    """
    if busqueda2:
        campana = Campana.objects.filter(
            Q(cam_detalles__icontains = busqueda2)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()

    if busqueda3:
        campana = Campana.objects.filter(
            Q(cam_descripcion__icontains = busqueda3)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()

    if busqueda4:
        """
        campana = Campana.objects.filter(
            Q(user__id == busqueda4)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
        """
        campana = Campana.objects.filter(Q(cam_creador__username__icontains = busqueda4))
        #DataPribadiSiswa.objects.filter(siswa_kelas__some_name__icontains=keyword2))
    

    data = {

        'marca_list' : marca_list,
        'campana' : campana,
        'lista_de_categorias' : lista_de_categorias,
        'color': color,
    }
    if request.user.is_authenticated:
        pass

    else:
        return redirect('login')

    return render(request,'app/interacciones.html',data)

def interacciones_detalles(request, id):

    

    print(request.user)

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    inter = Interaccion.objects.filter( int_usu_id = request.user )
    
    
    
    inter_list = inter.values_list('int_cam_id',flat=True)
    
    inter_list = list(inter_list)

    lista_estado = []

    for i in range(len(inter_list)):
        estado = Interaccion.objects.get ( Q(int_cam_id = inter_list[i] ) & Q(int_usu_id = request.user) )
        print("estado de la interaccion", inter_list[i] , estado.int_est_id.id)
        lista_estado.append([inter_list[i],estado.int_est_id.id])

    print("LISTA ESTADO", lista_estado)

    print("LISTA INTER", inter_list)

    marca = Marca.objects.get( mar_creador = id )
    
    print("MARCA", marca.mar_categoria)

    busqueda = request.POST.get("buscar")
    #busqueda1 = request.POST.get('buscar1', '')
    busqueda2 = request.POST.get("buscar2")
    busqueda3 = request.POST.get("buscar3")
    busqueda4 = request.POST.get("buscar4")

    campana = Campana.objects.filter( Q(id__in = inter_list) & Q(cam_creador = id) ).order_by('-id')

    cam = campana

    print(cam)
    cam_list = cam.values_list('cam_creador', flat=True)
    print(cam_list)
    cam_list=list(cam_list)
    print("camlist: ", cam_list)
    cam_list = list(set(cam_list))
    print("cam list: ", cam_list)

    marca_list = Marca.objects.filter(mar_creador__in = cam_list).order_by('-id')
    print(marca_list)
    print("marca list:", marca_list)




    lista_de_categorias = campana.values_list('cam_categoria', flat=True)
    print(lista_de_categorias)
    lista_de_categorias = list(set(lista_de_categorias))
    print(lista_de_categorias)

    if busqueda:
        campana = Campana.objects.filter(
            Q(cam_nombre__icontains = busqueda) #|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
    """
    if busqueda1:
        campana = Campana.objects.filter(
            Q(cam_creador__busqueda1__icontains = busqueda1)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
    """
    if busqueda2:
        campana = Campana.objects.filter(
            Q(cam_detalles__icontains = busqueda2)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()

    if busqueda3:
        campana = Campana.objects.filter(
            Q(cam_descripcion__icontains = busqueda3)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()

    if busqueda4:
        """
        campana = Campana.objects.filter(
            Q(user__id == busqueda4)#|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            
        ).distinct()
        """
        campana = Campana.objects.filter(Q(cam_creador__username__icontains = busqueda4))
        #DataPribadiSiswa.objects.filter(siswa_kelas__some_name__icontains=keyword2))
    

    data = {

        'marca_list' : marca_list,
        'campana' : campana,
        'lista_de_categorias' : lista_de_categorias,
        'marca': marca,
        'lista_estado': lista_estado,
        'color': color,
    }

    return render(request,'app/interacciones_detalles.html',data)

def contacto(request):
    data = {
        'form':ContactoForm()
    }
    """
    send_mail(
                    "Bienvenido a Uniperz",
                    "Las marcas que a ti te interesan con las condiciones que tú elijas",
                    'no-reply@uniperz.com' ,
                    [request.user.email],
                    fail_silently=False,
                    )
    """

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():

            formulario.save()
            data["mensaje"] = "contacto guardado"
        else:
            data["form"] = formulario

    return render(request,'app/contacto.html',data)
#@login_required
def galeria(request):
    return render(request,'app/galeria.html')

def agregar_producto(request):

    usuario = request.user
    print("id usuario",usuario)

    data = {
        'form' : ProductoForm(),
    }

    if request.method == 'POST':

        formulario = ProductoForm(data=request.POST, files = request.FILES)

        if formulario.is_valid():

            autor = formulario.save(commit=False)
            autor.pro_creador = usuario
            autor.save()
            formulario.save_m2m()
            messages.success(request, "Campaña Registrada")

        else:

            data["form"]=formulario

    return render(request,'app/productos_marca/agregar_producto.html',data)

@permission_required('app.add_campana')
def agregar_campana(request):
    #print("entra")
    usuario = request.user
    print("id usuario",usuario)

    marca = Marca.objects.filter(mar_creador = request.user)
    marca = marca.first()

    

    data = {

        'form': CampanaForm(),
        'form2': CalificarForm(),
        'form3': CompartirForm(),
        'form4': RecomendarForm(),
        'marca': marca,
    }

    if request.method == 'POST':

        if '_preview' in request.POST:
            print("preview campaña")

        formulario = CampanaForm(data=request.POST,files=request.FILES)
        formulario2 = CalificarForm(data=request.POST)
        formulario3 = CompartirForm(data=request.POST)
        formulario4 = RecomendarForm(data=request.POST)

        if formulario.is_valid() and formulario2.is_valid() and formulario3.is_valid() and formulario4.is_valid() :

            print("FORMULARIOS VALIDOSSSSSSSSS")
            autor = formulario.save(commit=False)
            autor.cam_creador = usuario
            autor.save()
            formulario.save_m2m()

            califica = formulario2.save(commit=False)
            califica.cal_cam_id = Campana.objects.get(id=autor.id)

            comparte = formulario3.save(commit=False)
            comparte.com_cam_id = Campana.objects.get(id=autor.id)

            recomienda = formulario4.save(commit=False)
            recomienda.rec_cam_id = Campana.objects.get(id=autor.id)

            """
            print("califica",califica.booleano)
            print("comparte",comparte.booleano)
            print("recomienda",recomienda.booleano)
            """
            medallas_totales = 0
            dias_totales = 0

            print(califica.cal_booleano)
            print(comparte.com_booleano)
            print(recomienda.rec_booleano)

            if califica.cal_booleano == True:

                medallas_totales = medallas_totales + califica.cal_medallas
                dias_totales = dias_totales + califica.cal_dias

            if comparte.com_booleano == True:

                medallas_totales = medallas_totales + comparte.com_medallas
                dias_totales = dias_totales + comparte.com_dias

            if recomienda.rec_booleano == True:

                medallas_totales = medallas_totales + recomienda.rec_medallas
                dias_totales = dias_totales + recomienda.rec_dias

            autor = formulario.save(commit=False)
            autor.cam_medallas = medallas_totales
            autor.cam_dias = dias_totales
            autor.save()

            #####

            

            print("")
            print("nombre archivo csv: \"", autor.cam_csv,"\"") #se intenta buscar el nombre del archivo del csv
            print("")
            print(str(autor.cam_csv))

            fichero = settings.MEDIA_ROOT+"\\"+ str(autor.cam_csv)
            print(fichero)
            print(leer_fichero(fichero))
            largo_lista = len(leer_fichero(fichero))
            
            
            
            autor.cam_cantidad_recompensas = largo_lista
            autor.save()

            #####

            califica.save()
            formulario2.save_m2m()

            comparte.save()
            formulario3.save_m2m()

            recomienda.save()
            formulario4.save_m2m()

            print("paso")
            messages.success(request, "Campaña Registrada")
            
            return redirect('listar_campanas')
        else:
            print("NO ENTROOOOO")
            data["form"]=formulario
            data["form2"]=formulario2
            data["form3"]=formulario3
            data["form4"]=formulario4

    return render(request,'app/producto/agregar.html',data)

@login_required
def desafio1(request, slug_text):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.get(slug=slug_text)
    #print("campana :", campana)
    #print("campana tiene el id: ",campana.id)

    calificar = Calificar.objects.get(cal_cam_id=campana.id)
    print("pregunta1 :", calificar.cal_pregunta)



    data = {

            'form': Int_CalificarForm(),
            'calificar': calificar,
            'color': color,

    }



    if request.method == 'POST':

        formulario = Int_CalificarForm(data=request.POST)

        if formulario.is_valid():
            """
            instance = formulario.save(commit=False)
            interaccion.respuesta1 = instance.respuesta1
            #print("respuesta interaccion",instance.respuesta1)
            #print("respuesta pre formulario",interaccion.respuesta1)
            interaccion.desafio1 = True
            print(interaccion.desafio1)
            interaccion.save()

            """
            inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)
            instance_intcal = formulario.save(commit=False)
            intcal = Int_Calificar.objects.get(intcal_int_id=inter.id)
            intcal.intcal_desafio = True
            intcal.intcal_respuesta = instance_intcal.intcal_respuesta
            #intcal.intcal_int_id = inter.id
            #print("respuesta del intcal",intcal.intcal_int_id)

            today = datetime.now() #nuevo
            intcal.intcal_fecha_int = today #nuevo

            intcal.save()

            messages.success(request, "Desafío Completado")

            return redirect(to="interacciones")

        else:

            data["form"] = formulario



    return render(request, 'app/desafio1.html', data)

@login_required
def desafio2(request, slug_text):
    #print("slug", slug_text)
    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.get(slug=slug_text)
    #interaccion = Interaccion.objects.get(campana_id=campana.id)
    inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)
    intcom = Int_Compartir.objects.get(intcom_int_id=inter.id)
    intcom.intcom_desafio = True
    #print(intcom.intcom_desafio)

    today = datetime.now() #nuevo
    intcom.intcom_fecha_int = today #nuevo
    
    intcom.save()

    data = {

        'slug_text' : slug_text,
        #'interaccion_activa': interaccion_activa,
        'color': color,

    }

    return render(request, 'app/desafio2.html', data)


@login_required
def desafio3(request, slug_text):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.get(slug=slug_text)
    lista_inter_id = Interaccion.objects.filter(int_cam_id = campana.id).values_list('id', flat=True)
    lista_inter_id = list(lista_inter_id)
    print(lista_inter_id)
    #lista_inter_correo = Interaccion.objects.filter(int_cam_id = campana.id).values_list('int', flat=True)
    

    data = {

        'form3' : Int_RecomendarForm(),
        'color': color,
    }
    

    if request.method == 'POST':

        formulario = Int_RecomendarForm(data=request.POST)

        correo = request.POST.get('intrec_respuesta')
        print("el correo que entra es: ", correo)
        existe = Int_Recomendar.objects.filter(
            Q(intrec_desafio = 1) & 
            ~Q(intrec_respuesta = '') & 
            Q(intrec_respuesta = correo) &
            Q(intrec_int_id__in = lista_inter_id)

            ).exists()
        
        if existe:
            #print("existe")
            messages.warning(request,"El correo ya existe")
            #messages.medallas(request,"El correo ya existe")
            #return redirect('desafio3', slug_text)
            
        else:

            if formulario.is_valid():

                inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)
                instance_intrec = formulario.save(commit=False)

                intrec = Int_Recomendar.objects.get(intrec_int_id=inter.id)
                print("respuesta correo", intrec.intrec_respuesta)
                intrec.intrec_desafio = True
                intrec.intrec_respuesta = instance_intrec.intrec_respuesta

                print(intrec.intrec_respuesta)

                today = datetime.now() #nuevo
                intrec.intrec_fecha_int = today #nuevo

                #intcal.intcal_int_id = inter.id
                #print("respuesta del intcal",intcal.intcal_int_id)
                intrec.save()










                print("link", request.get_full_path())
                print("campana",campana.slug)
                link = "http://127.0.0.1:8000"+str(request.get_full_path())[:-9]

                
                print("")
                print(str(request.user)+" te invita a Uniperz")
                
                print("responde esta campaña y recibirás premios, cupones, y descuentos "+"\n"+"ingresa a este link a continuación: "+str(link))
                print([intrec.intrec_respuesta])
                #email = EmailMessage()

                send_mail(
                    str(request.user)+" te invita a Uniperz",
                    "responde esta campaña y recibirás premios, cupones, y descuentos "+"\n"+"ingresa a este link a continuación: "+str(link),
                    'no-reply@uniperz.com' ,
                    [intrec.intrec_respuesta],
                    fail_silently=False,
                    )


                messages.info(request, "Has conseguido")
                #sweetify.sweetalert(request, 'Title', button=True)
                return redirect(to="interacciones")

            else:
                data["form3"]=formulario


    return render(request, 'app/desafio3.html', data)

"""
def desafio3(request, slug_text):
    
    campana = Campana.objects.get(slug=slug_text)
    #inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)
    

    data = {
        
        'form3' : Int_RecomendarForm()
    }
    
    if request.method == 'POST':
        
        formulario = Int_RecomendarForm(data=request.POST)

        
        if formulario.is_valid():
            
            inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)
            instance_intrec = formulario.save(commit=False)
            
            intrec = Int_Recomendar.objects.get(intrec_int_id=inter.id)
            print("respuesta correo", intrec.intrec_respuesta)
            intrec.intrec_desafio = True
            intrec.intrec_respuesta = instance_intrec.intrec_respuesta
            
            print(intrec.intrec_respuesta)
            #intcal.intcal_int_id = inter.id
            #print("respuesta del intcal",intcal.intcal_int_id)
            intrec.save()

            

            
            
            
            
            
            
            
            print("link", request.get_full_path())
            print("campana",campana.slug)
            link = "http://127.0.0.1:8000"+str(request.get_full_path())[:-8]
            
            print("link de la campana",link)

            send_mail(
                str(request.user)+" te invita a Uniperz",
                "responde esta campaña y recibirás premios, cupones, y descuentos "+"\n"+"ingresa a este link a continuación: "+str(link), 
                "no-reply@uniperz.com" , 
                [intrec.intrec_respuesta], 
                fail_silently=False,
                )

            
            messages.success(request, "Desafío Completado")

            return redirect(to="interacciones")

        else:
            data["form"]=formulario
    
    
    return render(request, 'app/desafio3.html', data)

"""

@login_required
def desafio4(request, slug_text):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    data = {

        'desafio4' : 'desafio4',
        'color': color,
    }


    return render(request, 'app/desafio4.html', data)

@permission_required('app.view_campana')

def listar_campanas(request):


    campanas = Campana.objects.filter(cam_creador=request.user)

    for campana in campanas:

        if campana.cam_fecha_inicio <= date.today() <= campana.cam_fecha_termino:
            print("cambia a Activo")
            campana.cam_estado = 2
            campana.save()
        elif date.today() > campana.cam_fecha_termino:
            print("cambia a Finalizado")
            campana.cam_estado = 3
            campana.save()
        elif date.today() < campana.cam_fecha_inicio:
            print("cambia a Pendiente")
            campana.cam_estado = 1
            campana.save()


    marca = Marca.objects.filter(mar_creador = request.user)
    marca = marca.first()
    print("MARCA",marca)
    print(campanas)
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(campanas,10)
        campanas = paginator.page(page)

    except:
        raise Http404

    data={

        'entity': campanas,
        'paginator': paginator,
        'marca': marca,

    }

    return render(request,'app/producto/listar.html',data)


def listar_productos(request):

    productos = Producto.objects.filter(pro_creador=request.user)
    print(productos)
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(productos,10)
        productos = paginator.page(page)
    
    except:
        raise Http404

    data={

        'entity': productos,
        'paginator': paginator

    }

    return render(request,'app/productos_marca/listar_productos.html',data)


@login_required
def detalles(request, slug_text):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(slug=slug_text)

    recompensa = None

    #inter = Interaccion.objects.get(campana_id = campana.id, usuario_id = request.user)

    if campana.exists():
        print("campana existe")
        campana = campana.first()
        marca = Marca.objects.get(mar_creador = campana.cam_creador)
        today = datetime.now()

        """
        print("FECHA ACTUAL:",date.today())
        print("FECHA TERMINO:",campana.cam_fecha_termino)

        if (date.today() <= campana.cam_fecha_termino):
            print("aun queda")
        else:
            print("fuiste weno")

        print("fecha y hora: ",today)
        """

        interaccion = Interaccion.objects.filter(int_cam_id = campana.id, int_usu_id = request.user)

        jugadores = list(Interaccion.objects.filter(int_cam_id = campana.id, int_est_id = 1))
        total_jugadores = list(Interaccion.objects.filter(int_cam_id = campana.id))
        total_jugadores = len(total_jugadores)
        jugadores_con_recompensa = list(Interaccion.objects.filter(int_cam_id = campana.id, int_est_id = 3))
        cantidad_jugadores=len(jugadores)
        cantidad_jugadores_con_recompensa = len(jugadores_con_recompensa)

        print("jugadores con recompensa", cantidad_jugadores_con_recompensa)
        campana.cam_cantidad_recompensas_canjeadas = cantidad_jugadores_con_recompensa
        campana.save()
        """
        desafio1 = Calificar.objects.get(id_campana=campana.id)
        desafio2 = Compartir.objects.get(id_campana=campana.id)
        desafio3 = Recomendar.objects.get(id_campana=campana.id)

        print("desafio1",desafio1.califica_o_no)
        print("desafio2",desafio2.comparte_o_no)
        print("desafio3",desafio3.recomienda_o_no)
        """
        print(campana.cam_cantidad_recompensas_canjeadas," < ",campana.cam_cantidad_recompensas )

        if interaccion.exists():



            interaccion_activa = True
            inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)
            print("interaccion existe")
            print("interaccion:", campana.id, request.user)

            instance_cal = Calificar.objects.get(cal_cam_id=campana.id)
            instance_com = Compartir.objects.get(com_cam_id=campana.id)
            instance_rec = Recomendar.objects.get(rec_cam_id=campana.id)

            lista_inter = []

            if instance_cal.cal_booleano == True:

                instance_intcal = Int_Calificar.objects.get(intcal_int_id=inter.id)
                print("respuesta del intcal",instance_intcal.intcal_desafio)
                lista_inter.append(['Calificar',instance_cal.cal_medallas,instance_cal.cal_dias, instance_intcal.intcal_desafio, instance_intcal.intcal_fecha_inicio, instance_intcal.intcal_fecha_limite])

            if instance_com.com_booleano == True:

                instance_intcom = Int_Compartir.objects.get(intcom_int_id=inter.id)
                print("respuesta del intcom",instance_intcom.intcom_desafio)
                lista_inter.append(['Compartir',instance_com.com_medallas ,instance_com.com_dias , instance_intcom.intcom_desafio, instance_intcom.intcom_fecha_inicio, instance_intcom.intcom_fecha_limite])

            if instance_rec.rec_booleano == True:

                instance_intrec = Int_Recomendar.objects.get(intrec_int_id=inter.id)
                print("respuesta del intrec",instance_intrec.intrec_desafio)
                lista_inter.append(['Recomendar',instance_rec.rec_medallas,instance_rec.rec_dias , instance_intrec.intrec_desafio, instance_intrec.intrec_fecha_inicio, instance_intrec.intrec_fecha_limite])

            print("lista de interacciones", lista_inter)
            print("largo de la lista: ",len(lista_inter))
            """
            for i in range(len(lista_inter)):
                if i+1 < len(lista_inter):
                    print(lista_inter[i][0],lista_inter[i+1][0])
            """

                #print(i)


            hay_recompensa_o_no = True
            
            #hay_recompensa_o_no = False
            print("estado interaccion",inter.int_est_id)
            
            entra_if=0

            if inter.int_est_id == Estado.objects.get(id = 1):
                print("entra este primer if")
                for i in range(len(lista_inter)):
                    print(lista_inter[i][3])
                    if lista_inter[i][3] == False:
                        num = i
                        
                        entra_if=1
                        break
                #print(num)
                

                if entra_if == 1:

                    if today > lista_inter[num][5]:
                        print("Inactivo")
                        inter.int_est_id = Estado.objects.get(id = 2)
                        print("estado interaccion",inter.int_est_id) #finalizado
                        inter.save()
                    else:
                        print("activo")

                elif entra_if == 0:
                    print("no entró")

            if inter.int_est_id != Estado.objects.get(id = 3):

                #hay_recompensa_o_no = True

                for i in range(len(lista_inter)):

                    if lista_inter[i][3] == False:

                        hay_recompensa_o_no = False

                print("HAY RECOMPENSA O NO:", hay_recompensa_o_no)

                if hay_recompensa_o_no == True:

                    print("ENTRA AL IF DE LAS CANTIDAD DE RECOMPENSA")


                    print("estado interaccion",inter.int_est_id) #finalizado

                    inter.int_est_id = Estado.objects.get(id = 3)
                    print("estado interaccion",inter.int_est_id) #finalizado
                    inter.save()
                    print("recompensa post bucle ",inter.int_recompensa)
                    if campana.cam_cantidad_recompensas_canjeadas < campana.cam_cantidad_recompensas and inter.int_recompensa == False:


                        
                        campana.cam_cantidad_recompensas_canjeadas = campana.cam_cantidad_recompensas_canjeadas + 1
                        campana.save()
                        inter.int_num_recompensa = campana.cam_cantidad_recompensas_canjeadas
                        inter.int_recompensa = True
                        inter.save()

                        if campana.cam_cantidad_recompensas_canjeadas == campana.cam_cantidad_recompensas:
                            
                            print("se cambia a finalizado, se llenan los cupos")
                            campana.estado = 3
                            campana.save()

                        #print(campana.cam_cantidad_recompensas_canjeadas," < ",campana.cam_cantidad_recompensas )
                        
                        #ESTA PARTE PUEDE APUNTA AL DIRECTORIO DE MEDIA
                        fichero_campana = settings.MEDIA_ROOT+"\\"+ str(campana.cam_csv)
                        #print(fichero_campana)
                        lista_recom = leer_fichero(fichero_campana)
                        print("LISTA RECOMPENSAS: ",lista_recom)
                        recompensa = lista_recom[inter.int_num_recompensa - 1][0]

                        print("int_num_recompensa",inter.int_num_recompensa)

                    else:

                        print("recompensas llenas")

                    

                else:
                    recompensa = None

            if inter.int_est_id == Estado.objects.get(id = 3):

                print("ENTRA AL IF DE LAS CANTIDAD DE RECOMPENSA")
                fichero_campana = settings.MEDIA_ROOT+"\\"+ str(campana.cam_csv)
                #print(fichero_campana)
                lista_recom = leer_fichero(fichero_campana)
                print("LISTA RECOMPENSAS: ",lista_recom)
                recompensa = lista_recom[inter.int_num_recompensa - 1][0]
                print("LA RECOMPENSA ES: ",recompensa)



        else:

            print("interaccion no existe")
            inter = None
            interaccion_activa = False
            lista_inter = []


            
            print("interaccion no existe")
            print("interaccion:", campana.id, request.user)

            cal = Calificar.objects.get(cal_cam_id=campana.id)
            com = Compartir.objects.get(com_cam_id=campana.id)
            rec = Recomendar.objects.get(rec_cam_id=campana.id)

            

            if cal.cal_booleano == True:

                
                lista_inter.append(['Calificar',cal.cal_medallas,cal.cal_dias])

            if com.com_booleano == True:

                
                lista_inter.append(['Compartir',com.com_medallas ,com.com_dias])

            if rec.rec_booleano == True:

                lista_inter.append(['Recomendar',rec.rec_medallas,rec.rec_dias])

            print("lista de interacciones", lista_inter)


    else:
        return HttpResponse("<h1>Pagina no encontrada</h1>")



    print("campaña",campana.id)
    print("usuario",request.user)



    if request.method == 'POST':

        lista_inter=[]

        instance = Interaccion(int_usu_id=request.user)

        instance.int_cam_id = Campana.objects.get(id=campana.id)

        instance.save()
        print("pasa el save")
        interaccion_activa = True

        inter = Interaccion.objects.get(int_cam_id = campana.id, int_usu_id = request.user)

        instance_cal = Calificar.objects.get(cal_cam_id=campana.id)
        instance_com = Compartir.objects.get(com_cam_id=campana.id)
        instance_rec = Recomendar.objects.get(rec_cam_id=campana.id)
        #instance_cal.int_cam_id = Campana.objects.get(id=campana.id)
        print("booleano calificar",instance_cal.cal_booleano)
        print("booleano compartir",instance_com.com_booleano)
        print("booleano recomendar",instance_rec.rec_booleano)

        print("id de la interaccion", instance.id)

        if instance_cal.cal_booleano == True:

            lista_inter.append(['Calificar',instance_cal.cal_medallas,instance_cal.cal_dias,False])

            instance_intcal = Int_Calificar()
            instance_intcal.intcal_int_id = Interaccion.objects.get(id=instance.id)
            instance_intcal.save()

        if instance_com.com_booleano == True:

            lista_inter.append(['Compartir',instance_com.com_medallas ,instance_com.com_dias ,False])

            instance_intcom = Int_Compartir()
            instance_intcom.intcom_int_id = Interaccion.objects.get(id=instance.id)
            instance_intcom.save()

        if instance_rec.rec_booleano == True:

            lista_inter.append(['Recomendar', instance_rec.rec_medallas , instance_rec.rec_dias ,False])

            instance_intrec = Int_Recomendar()
            instance_intrec.intrec_int_id = Interaccion.objects.get(id=instance.id)
            instance_intrec.save()

        print("lista de interacciones", lista_inter)

        if len(lista_inter) > 0:

            cont_dias = 0
            today = datetime.now()
            print("-------")

        #Calificar.objects.get(id_campana = campana.id)


            for i in range(len(lista_inter)):

                print("contador de dias",cont_dias)

                if lista_inter[i][0] == 'Calificar':

                    print("dias cal:",instance_cal.cal_dias)
                    instance_intcal.intcal_fecha_inicio = today + timedelta(days = cont_dias)
                    instance_intcal.intcal_fecha_limite = instance_intcal.intcal_fecha_inicio + timedelta(days = instance_cal.cal_dias)


                    print("fecha inicio intcal:", instance_intcal.intcal_fecha_inicio)
                    print("fecha limite intcal:", instance_intcal.intcal_fecha_limite)
                    instance_intcal.save()

                    cont_dias = cont_dias + instance_cal.cal_dias

                if lista_inter[i][0] == 'Compartir':

                    print("dias com:",instance_com.com_dias)
                    instance_intcom.intcom_fecha_inicio = today + timedelta(days = cont_dias)
                    instance_intcom.intcom_fecha_limite = instance_intcom.intcom_fecha_inicio + timedelta(days = instance_com.com_dias)

                    print("fecha inicio intcom:", instance_intcom.intcom_fecha_inicio)
                    print("fecha limite intcom:", instance_intcom.intcom_fecha_limite)
                    instance_intcom.save()

                    cont_dias = cont_dias + instance_com.com_dias

                if lista_inter[i][0] == 'Recomendar':

                    print("dias rec:",instance_rec.rec_dias)
                    instance_intrec.intrec_fecha_inicio = today + timedelta(days = cont_dias)
                    instance_intrec.intrec_fecha_limite = instance_intrec.intrec_fecha_inicio + timedelta(days = instance_rec.rec_dias)
                    cont_dias = cont_dias + instance_rec.rec_dias
                    print("fecha inicio intrec:", instance_intrec.intrec_fecha_inicio)
                    print("fecha limite intrec:", instance_intrec.intrec_fecha_limite)

                    instance_intrec.save()

                    cont_dias = cont_dias + instance_rec.rec_dias

            print("dias contados",cont_dias)
            cont_dias = 0


    print("interaccion:", interaccion_activa)


    context = {

        'campana': campana,
        'interaccion_activa': interaccion_activa,
        'inter': inter,
        'lista_inter': lista_inter,
        'hoy': today,
        'cantidad_jugadores': cantidad_jugadores,
        'cantidad_jugadores_con_recompensa' : cantidad_jugadores_con_recompensa,
        'marca': marca,
        'recompensa' : recompensa,
        'total_jugadores' : total_jugadores,
        'color': color,
    }


    return render(request, 'app/detalles.html', context)

def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="listar_productos")
        """
        else:
            print("sale")
        """
        data["form"] = formulario


    return render(request, 'app/productos_marca/modificar_producto.html',data)

@permission_required('app.change_campana')
def modificar_campana(request, id):

    marca = Marca.objects.filter(mar_creador=request.user)
    marca = marca.first()
    campana = get_object_or_404(Campana, id=id)
    

    data = {
        'marca': marca,
        'form': CampanaForm(instance=campana),
        
    }

    if request.method == 'POST':
        formulario = CampanaForm(data=request.POST, instance=campana, files=request.FILES)
        if formulario.is_valid():

            autor = formulario.save(commit=False)

            #####

            

            print("")
            print("nombre archivo csv: \"", autor.cam_csv,"\"") #se intenta buscar el nombre del archivo del csv
            print("")
            print(str(autor.cam_csv))

            fichero = settings.MEDIA_ROOT+"\\"+ str(autor.cam_csv)
            print("RUTA DEL FICHERO:",fichero)
            print(leer_fichero(fichero))
            largo_lista = len(leer_fichero(fichero))
            
            
            
            autor.cam_cantidad_recompensas = largo_lista
            autor.save()

            #####

            formulario.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="listar_campanas")
        """
        else:
            print("sale")
        """
        data["form"] = formulario


    return render(request, 'app/producto/modificar.html',data)

@permission_required('app.delete_campana')
def eliminar_campana(request,id):
    campana = get_object_or_404(Campana, id=id)
    campana.delete()
    messages.success(request, "eliminado correctamente")
    return redirect(to="listar_campanas")

def eliminar_producto(request,id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "eliminado correctamente")
    return redirect(to="listar_productos")

def caracteristicas(request):

    print(request.user)

    data ={
        'form':CaracteristicasForm(),
        
    }

    if not request.user.is_authenticated:

        return redirect('login')
    
    grupo = request.user.groups.all()

    if grupo: 

        grupo = list(grupo)
        grupo = str(grupo[0])
        #print(grupo)

        if grupo == 'Marca':
                
            marca = Marca.objects.filter(mar_creador = request.user)
            marca = marca.first()
            print("es marca")
            return redirect('listar_campanas')
            
        elif grupo == 'Usuario':

            caract = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id).exists()
    
            if not caract:

                messages.warning(request, "Debe usted ingresar sus datos")
                    
                #return redirect('caracteristicas')
                    
            else:
                    
                print("no pasa nada, todo bien")

        else:
            print("que?")


    usuario = request.user

    if request.method == 'POST':

        formulario = CaracteristicasForm(data=request.POST)
        
        if formulario.is_valid():

            autor = formulario.save(commit=False)
            autor.car_usu_usu_id = usuario

            autor.save()
            formulario.save()

            

            messages.success(request, "caracteristicas agregadas correctamente")
            #return redirect(to="home")
            return redirect(to="seleccionar_categorias")

        data["form"] = formulario

    return render(request,'registration/caracteristicas.html',data)

def seleccionar_categorias(request):

    print(request.user)

    lista_categorias = Categoria.objects.all().order_by('id').values_list( 'id','cat_nombre')
    lista_categorias = list(lista_categorias)
    print(lista_categorias)

    lista_lista = []

    existe = Seleccion_Categorias_Usuario.objects.filter(sel_cat_usu_id = request.user.id).exists()
    res = []

    if existe:

        print("existe")
        lista_llamada = Seleccion_Categorias_Usuario.objects.get(sel_cat_usu_id = request.user.id)
        print(lista_llamada.sel_cat_cat)
        lista_llamada = lista_llamada.sel_cat_cat
        res = ast.literal_eval(lista_llamada)
        print("resultado: ",res)
    
    else:

        print("no esite")
        objeto = Seleccion_Categorias_Usuario.objects.create(sel_cat_usu_id_id=request.user.id, sel_cat_cat="[]")
        objeto.save()

    print(lista_categorias)

    if len(res) == 0:

        for i in range(len(lista_categorias)):
            lista_lista.append([lista_categorias[i][0] , lista_categorias[i][1] , 0])

    elif len(res) > 0:

        for i in range(len(lista_categorias)):

            if i in res:
                print(i)
                lista_lista.append([lista_categorias[i][0] , lista_categorias[i][1] , 1])

            else:

                lista_lista.append([lista_categorias[i][0] , lista_categorias[i][1] , 0])

                    
    else:

        pass

    print(lista_lista)

    data = {
        
        'lista_lista': lista_lista,
        'list': list,
    }

    


    if not request.user.is_authenticated:

        return redirect('login')
    
    grupo = request.user.groups.all()

    if grupo: 

        grupo = list(grupo)
        grupo = str(grupo[0])
        #print(grupo)

        if grupo == 'Marca':
                
            marca = Marca.objects.filter(mar_creador = request.user)
            marca = marca.first()
            print("es marca")
            return redirect('listar_campanas')
            
        elif grupo == 'Usuario':

            sel = Seleccion_Categorias_Usuario.objects.filter(sel_cat_usu_id = request.user.id).exists()
    
            if not sel:

                messages.warning(request, "Debe usted ingresar sus datos")
                    
                #return redirect('caracteristicas')
                    
            else:
                    
                print("no pasa nada, todo bien")

        else:
            print("que?")


    usuario = request.user

    if request.method == 'POST':

        lista = request.POST.getlist('lista')
        print("la lista de lo que ingresaste es: ",lista)
        lista_nueva = []
        if len(lista) > 0:
            for i in range(len(lista)):
                print(lista[i])
                lista_nueva.append(int(lista[i]))

        elif len(lista) == 0:
            messages.warning(request, "debes agregar por lo menos una categoría")
            return redirect(to="seleccionar_categorias")
        
        lista = str(lista_nueva)
        print("lista en str", lista)

        lista_salida = Seleccion_Categorias_Usuario.objects.get(sel_cat_usu_id = request.user.id)
        lista_salida.sel_cat_cat = lista
        lista_salida.save()
        messages.success(request, "categorías agregadas correctamente")
        return redirect('home')

    return render(request,'registration/seleccionar_categorias.html',data)


def politicas_privacidad(request):

    return render(request,'registration/politicas_privacidad.html')

def registro(request):

    data={
        'form': CustomUserCreationForm(),
        #'form2': Perfil_UsuarioForm(),
    }

    if request.method == 'POST':

        formulario = CustomUserCreationForm(data=request.POST)
        #formulario2 = Perfil_UsuarioForm(data=request.POST)


        if formulario.is_valid():

            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            
            """
            marca = models.Marca(
                
                id=id,
                mar_creador=request.user.id,
                mar_nombre=request.user.first_name,
                mar_apellido=request.user.last_name,
                mar_mail=request.user.email,

                
            )
            marca.save()
            """
            #usuario = request.user

            #print("el usuario a loguear es",usuario)
            #instancia_perfil = formulario2.save(commit=False)
            #instancia_perfil.per_usu_usu_id = usuario
            #instancia_perfil.save()
            #formulario2.save_m2m()


            grupo = Group.objects.get(name='Usuario')
            print(user.username,"se incorpora al grupo",grupo)
            user.groups.add(grupo)

            
            send_mail(
                    "Bienvenido a Uniperz "+str(user.username),
                    "Las marcas que a ti te interesan con las condiciones que tú elijas",
                    'no-reply@uniperz.com' ,
                    [user.email],
                    fail_silently=False,
                    )

            login(request,user)
            messages.success(request,"Te has registrado correctamente")
            return redirect(to="caracteristicas")
        data["form"] = formulario

    return render(request,'registration/registro.html',data)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'app/poll/create.html', context)

def vote(request, poll_id):

    #Revisar base de datos con el Poll
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'app/poll/vote.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'app/poll/results.html', context)




def preview(request):

    #Ver como guardar imagen >_>

    if request.method == 'POST':
        var = request.POST.dict()
        print(var)
        campana = var
        interaccion_activa = True
        inter = False
        lista_inter =[]
        cal_bool = 0
        com_bool = 0
        rec_bool = 0
        if 'cal_booleano' in var:
            if (var['cal_booleano'] == 'on'):
                cal_bool = 1
        if 'com_booleano' in var:
            if (var['com_booleano'] == 'on'):
                com_bool = 1
        if 'rec_booleano' in var:
            if (var['rec_booleano'] == 'on'):
                rec_bool = 1
        lista_inter.append(['Calificar', var['cal_medallas'], var['cal_dias'], cal_bool])
        lista_inter.append(['Compartir', var['com_medallas'], var['com_dias'], com_bool])
        lista_inter.append(['Recomendar', var['rec_medallas'], var['rec_dias'], rec_bool])

        context = {

            'campana': campana,
            'interaccion_activa': interaccion_activa,
            'inter': inter,
            'lista_inter': lista_inter,
        }

        #Guardar a base


    return render(request, 'app/preview.html', context)

    # todo: Cambiar agregar campaña desde el crispy form, ver cómo mantener estructura del crispy al confirmar del preview.


def age(year_usu,month_usu,day_usu):
    today = date.today()
    return today.year - year_usu - ((today.month, today.day) < (month_usu, day_usu))

def dashboard_campana(request,id):

    campana = get_object_or_404(Campana, id=id)
    #print("nombre campana: ",campana.cam_nombre)
    
    print("la id de la campaña es: ", id)
    marca = Marca.objects.filter(mar_creador=request.user)
    marca = marca.first()

    inter_campana = Interaccion.objects.filter(int_cam_id = id)
    

    activo = len(list(Interaccion.objects.filter(int_cam_id = campana.id, int_est_id = 1)))
    inactivo = len(list(Interaccion.objects.filter(int_cam_id = campana.id, int_est_id = 2)))
    completado = len(list(Interaccion.objects.filter(int_cam_id = campana.id, int_est_id = 3)))

    lista_estados = [activo, inactivo, completado]
    #print("LISTA ESTADOS",lista_estados)

    promedio_calificacion = None
    
    

    interacciones = Interaccion.objects.filter(int_cam_id_id = id)
    lista_int = interacciones.values_list('id', flat=True)
    print("LISTA DE INTERACCIONES QUE TIENEN EL ID DE LA CAMPAÑA: ",lista_int)
    lista_int = list(lista_int)
    #print(lista_int)
    
    calificaciones = Int_Calificar.objects.filter(Q(intcal_desafio = 1) & Q(intcal_int_id__in = lista_int )).values_list('intcal_respuesta', flat=True)
    calificaciones = list(calificaciones)
    #print("calificaciones: ",calificaciones)

    if calificaciones == []:
        cantidad_calificacion = 0 
        print("cant calificaciones: ",cantidad_calificacion)

    recomendaciones = Int_Recomendar.objects.filter(Q(intrec_desafio = 1) & Q(intrec_int_id__in = lista_int)) #.values_list('intrec_respuesta', flat=True)
    recomendaciones = len(list(recomendaciones))
    #print("recomendaciones: ", len(recomendaciones))

    desafio_rec = Recomendar.objects.get(rec_cam_id = campana.id)
    if desafio_rec.rec_booleano == 0:
        existe_rec = 0
    elif desafio_rec.rec_booleano == 1:
        existe_rec = 1
    else:
        pass

    print(existe_rec)
        

    
    if len(calificaciones) != 0:

        promedio_calificacion = 0

        for i in range(len(calificaciones)):

            promedio_calificacion = promedio_calificacion + calificaciones[i]

        promedio_calificacion = promedio_calificacion/len(calificaciones)
        print(promedio_calificacion)

        pregunta_calificar = Calificar.objects.filter(cal_cam_id = id).values_list('cal_pregunta',flat=True)
        pregunta_calificar = list(pregunta_calificar)
        print(pregunta_calificar[0])

        pregunta_calificacion = pregunta_calificar[0]
        cantidad_calificacion = len(calificaciones)
        lista_grafico_calificaciones = [0,0,0,0,0]

        for i in range(len(calificaciones)):
            if calificaciones[i] == 1:
                lista_grafico_calificaciones[0]=lista_grafico_calificaciones[0]+1
            elif calificaciones[i] == 2:
                lista_grafico_calificaciones[1]=lista_grafico_calificaciones[1]+1
            elif calificaciones[i] == 3:
                lista_grafico_calificaciones[2]=lista_grafico_calificaciones[2]+1
            elif calificaciones[i] == 4:
                lista_grafico_calificaciones[3]=lista_grafico_calificaciones[3]+1
            elif calificaciones[i] == 5:
                lista_grafico_calificaciones[4]=lista_grafico_calificaciones[4]+1
            else:
                print("algo no funca")

        #print(lista_grafico_calificaciones)

    else: 
        lista_grafico_calificaciones = [0,0,0,0,0]
        cantidad_calificacion = 0
        promedio_calificacion = None
        pregunta_calificacion = None
        cantidad_calificacion = None
    

    usuario = []
    Total_Usuarios = 0
    #Se agrega el usuario y sus caracteristicas a cada posición de la lista
    for ic in inter_campana:
        datos_base = User.objects.get(id = ic.int_usu_id_id)
        caracteristicas = Caracteristicas_Usuario.objects.get(car_usu_usu_id = ic.int_usu_id_id)
        estado = ic.int_est_id

        usuario.append({
            'datos_base':datos_base,
            'caracteristicas':caracteristicas,
            'estado': estado})
        Total_Usuarios += 1

    Contador_estados = {'Activa': 0, 'Inactiva': 0, 'Completada': 0}

    Total_Regiones = [i+[0] for i in models.opciones_regiones]

    

    Total_Edad = [0,0,0,0,0,0] #[15-24,25-34,35-44,45-54,55-64,65+]
    
    for u in usuario:
        #Get Edad y meterla en un rango
        #Get Región
        print('\n')
        caracteristicas = u['caracteristicas']
        datos_base = u['datos_base']
        print(f'\nUsuario: {datos_base}')
        fecha_nacimiento = caracteristicas.car_usu_fecha_nacimiento
        edad = age(fecha_nacimiento.year, fecha_nacimiento.month, fecha_nacimiento.day)
        region = caracteristicas.car_usu_region
        Total_Regiones[region][2] += 1
        print(f'Edad: {edad}\nRegion: {region}\nEstado:{estado}')
        if 15 <= edad <= 24:
            Total_Edad[0] += 1
        elif 25 <= edad <= 34:
            Total_Edad[1] += 1
        elif 35 <= edad <= 44:
            Total_Edad[2] += 1
        elif 45 <= edad <= 54:
            Total_Edad[3] += 1
        elif 55 <= edad <= 64:
            Total_Edad[4] += 1
        elif 65 <= edad:
            Total_Edad[5] += 1
        
    print(f'Total_Edad: {Total_Edad}\nTotal_Regiones: {Total_Regiones}')

    print("REGIONES TOTAAAAL",Total_Regiones)
    print("")
    print("LISTA ORDENADA:", sort_third(Total_Regiones))

    Total_Regiones_Ordenado = sort_third(Total_Regiones)

    while len(Total_Regiones_Ordenado) > 5:
        Total_Regiones_Ordenado.pop()

    print("SOLO CON 5",Total_Regiones_Ordenado)

    nombre_de_regiones = [item[1] for item in Total_Regiones_Ordenado]
    usuarios_en_regiones = [item[2] for item in Total_Regiones_Ordenado]
    
    for i in range(len(nombre_de_regiones)):

        if nombre_de_regiones[i] == "Region de Arica y Parinacota":
            nombre_de_regiones[i] = "Arica y Parinacota"
        elif nombre_de_regiones[i] == "Region de Tarapacá":
            nombre_de_regiones[i] = "Tarapacá"
        elif nombre_de_regiones[i] == "Region de Antofagasta":
            nombre_de_regiones[i] = "Antofagasta"
        elif nombre_de_regiones[i] == "Region de Atacama":
            nombre_de_regiones[i] = "Atacama"
        elif nombre_de_regiones[i] == "Region de Coquimbo":
            nombre_de_regiones[i] = "Coquimbo"
        elif nombre_de_regiones[i] == "Region de Valparaíso":
            nombre_de_regiones[i] = "Valpo"
        elif nombre_de_regiones[i] == "Region Metropolitana de Santiago":
            nombre_de_regiones[i] = "RM"
        elif nombre_de_regiones[i] == "Region del Libertador General Bernardo O'Higgins":
            nombre_de_regiones[i] = "O'Higgins"
        elif nombre_de_regiones[i] == "Region del Maule":
            nombre_de_regiones[i] = "Maule"
        elif nombre_de_regiones[i] == "Region del Ñuble":
            nombre_de_regiones[i] = "Ñuble"
        elif nombre_de_regiones[i] == "Region del Biobío":
            nombre_de_regiones[i] = "Biobío"
        elif nombre_de_regiones[i] == "Region de los Ríos":
            nombre_de_regiones[i] = "Ríos"
        elif nombre_de_regiones[i] == "Region de los Lagos":
            nombre_de_regiones[i] = "Lagos"
        elif nombre_de_regiones[i] == "Region de Aysén del General Carlos Ibáñez del Campo":
            nombre_de_regiones[i] = "Aysén"
        elif nombre_de_regiones[i] == "Region de Magallanes y de la Antártica Chilena":
            nombre_de_regiones[i] = "Magallanes y Antártica"
    """"""
    print("")
    print(nombre_de_regiones)
    print(usuarios_en_regiones)

    data = {
        'inter_campana':inter_campana.values(),
        'Total_Usuarios': Total_Usuarios,
        'Total_Edad': Total_Edad,
        'Total_Regiones': Total_Regiones,
        'lista_estados': lista_estados,
        'marca': marca,
        'campana': campana,
        'nombre_de_regiones': nombre_de_regiones,
        'usuarios_en_regiones': usuarios_en_regiones,
        'promedio_calificacion': promedio_calificacion,
        'pregunta_calificacion': pregunta_calificacion,
        'cantidad_calificacion': cantidad_calificacion,
        'lista_grafico_calificaciones': lista_grafico_calificaciones,
        'existe_rec': existe_rec,
        'recomendaciones': recomendaciones,

    }

    csv1=csvMaker(["15-24","25-34","35-44","45-54","55-64","65+"], [Total_Edad])
    Col_Regiones = [ i[1] for i in models.opciones_regiones]
    csv2=csvMaker(Col_Regiones, Total_Regiones)
    # return csv1
    # return csv2
    return render(request, 'app/producto/dashboard.html', data)

def csvMaker(request,data):
    response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    writer = csv.writer(response)
    for d in data:
        writer.writerow([i for i in d])
    return response

def Avatar(request):
    data = {
        'avatar': "tomaste datos"
    }

    return render(request,'app/Avatar.html', data)

def graficos(request):

    marca = Marca.objects.filter(mar_creador=request.user)

    data = {
       "marca": marca,
    }

    return render(request,'app/graficos.html', data)

def buscar(request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    buscado = 0
    campana = Campana.objects.filter(Q(cam_fecha_termino__gte = date.today()) & Q(cam_fecha_inicio__lte = date.today())).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))
        buscado = 1

    data = {
        'campana' : campana,
        'buscado' : buscado,
        'color': color,
    }

    return render(request,'app/buscar.html', data)

def marcas(request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    inter = Interaccion.objects.filter(int_usu_id = request.user)
    inter_list = inter.values_list('int_cam_id', flat=True)
    inter_list = list(inter_list)
    print("inter list: ",inter_list)
    print("----")
    lista_campana = []

    
    
    cam = Campana.objects.filter(id__in = inter_list)
    #cam_list = cam.values_list('cam_creador', flat=True)
    #cam_list = list(cam_list)
    print(cam)
    cam_list = cam.values_list('cam_creador', flat=True)
    print(cam_list)
    cam_list=list(cam_list)
    print("camlist: ", cam_list)
    cam_list = list(set(cam_list))
    print("cam list: ", cam_list)



    marca_list = Marca.objects.filter(mar_creador__in = cam_list).order_by('-id')
    
    #marca_list = list(marca_list)
    print(marca_list)
    print("marca list:", marca_list)

    

    lista_de_categorias = cam.values_list('cam_categoria', flat=True)
    print(lista_de_categorias)
    lista_de_categorias = list(set(lista_de_categorias))
    print(lista_de_categorias)

    busqueda = request.POST.get("buscar")
    busqueda_tecnologia = request.POST.get("buscar_tecnologia")

    if busqueda:

        marca_list = Marca.objects.filter(Q(mar_creador__username__icontains = busqueda) & Q(mar_creador__in = cam_list)).order_by('-id')
        
        cam = Campana.objects.filter(Q(id__in = inter_list) & Q(cam_creador__username__icontains = busqueda))
        print("post busqueda: ",cam)
        lista_de_categorias = cam.values_list('cam_categoria', flat=True)
        print(lista_de_categorias)
        lista_de_categorias = list(set(lista_de_categorias))
        print("FINAL FINAL",lista_de_categorias)
        
    print("busqueda tecnologia: ",busqueda_tecnologia)

    if busqueda_tecnologia:
        
        marca_list = Marca.objects.filter(Q(mar_categoria__id = 1) & Q(mar_creador__in = cam_list)).order_by('-id')
        




    
    

    data = {

        'marca_list' : marca_list,
        'lista_de_categorias' : lista_de_categorias,
        'color': color,
    }

    
    return render(request, 'app/marcas.html', data)
    #return render(request, 'app/marcas.html', data)

def conf_marca(request):

    marca = Marca.objects.filter(mar_creador=request.user)

    data = {
        'form':MarcaForm()
    }

    if marca.exists():

        print("marca existe")
        return redirect("modificar_marca", id = request.user.id )
    
    else:
        print("no tiene marca")
        pass

    if request.method == 'POST':

        formulario = MarcaForm(files=request.FILES)

        if formulario.is_valid():

            autor = formulario.save(commit=False)
            autor.mar_creador = request.user

            formulario.save()
            messages.success(request, "Imagen Subida")
            return redirect(to="home")

        else:
            data["form"] = formulario
        
        
    return render(request, 'app/conf_marca.html', data)

def modificar_marca(request, id):

    print("entra")

    #marca = get_object_or_404(Marca, mar_creador=id)
    marca = Marca.objects.get(mar_creador = id)
    #print("MARCA ID", marca.id)
    #print("MARCA CREADOR", marca.mar_creador)

    usuario = User.objects.get(username=marca.mar_creador)
    print("usuario: ",usuario)

    user = request.user

    data = {
        'form': MarcaForm(instance=marca),
        #'form2' : PasswordChangeForm(user),
        'marca': marca,
        'id' : request.user.id,
        
    }

    if request.method == 'POST':

        formulario = MarcaForm(instance=marca, files=request.FILES, data=request.POST)
        #formulario2 = PasswordChangeForm(request.user, request.POST)

        if formulario.is_valid():
            
            usuario.first_name = marca.mar_nombre
            usuario.last_name = marca.mar_apellido
            usuario.email = marca.mar_mail
            #print(marca.mar_nombre)
            usuario.save()
            formulario.save()
            #formulario2.save()
            messages.success(request, "modificado correctamente")
            #return redirect(to="home")
        
        else:
            print("saleeeeeeee")

        """

        if formulario2.is_valid():
            
            formulario2.save()
            #formulario2.save()
            messages.success(request, "modificado correctamente")
            #return redirect(to="home")
        
        else:
            print("salee")

        """

        data["form"] = formulario
        #data["form2"] = formulario2


    return render(request, 'app/modificar_marca.html',data)

def marca_cambiar_contrasena(request, id):

    #print("username: ", request.user.username)
    #print("password: ", request.user.password)
    #print(request.user.email)

    marca = Marca.objects.get(mar_creador = id)
    

    data = {
        'form' : PasswordChangeForm(request.user),
        'id' : request.user.id,
        'marca' : marca,
    }

    if request.method == 'POST':

        formulario = PasswordChangeForm(user=request.user, data=request.POST)
        #success_url = reverse_lazy()
        
        
        if formulario.is_valid():
            
            

            formulario.save()
            update_session_auth_hash(request, formulario.user)
            #formulario2.save()

            send_mail(
                    "Uniperz - Cambio de contraseña de "+str(request.user),
                    "Usted ha cambiado de contraseña",
                    'no-reply@uniperz.com' ,
                    [request.user.email],
                    fail_silently=False,
                    )
            

            messages.success(request, "Contraseña modificada correctamente")
            #return redirect(to="home")
        
        else:
            print("no cambia la contra")

        data["form"] = formulario

    

    return render(request, 'app/marca_cambiar_contraseña.html',data)

def marca_detalles(request, id):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    busqueda = request.POST.get("buscar")

    print(id)
    usuario = User.objects.get(username = id)
    print(usuario.id)

    usu_id = usuario.id
    
    #campana = Campana.objects.filter(cam_creador = usu_id)

    campana = Campana.objects.filter(Q(cam_fecha_termino__gte = date.today()) & Q(cam_fecha_inicio__lte = date.today()) & Q(cam_creador = usu_id)).order_by('-id')
    
    producto = Producto.objects.filter(pro_creador = usu_id)
    marca = Marca.objects.get(mar_creador = usu_id)
    

    print("campañas: ",campana)
    print("productos: ",producto)
    print("marca: ",marca)

    if busqueda:
        campana = Campana.objects.filter(
            Q(cam_nombre__icontains = busqueda) #|
            #Q(cam_cam_detalles__icontains = busqueda) |
            #Q(cam_descripcion__icontains = busqueda)
            & Q(cam_fecha_inicio__lte = date.today())
            & Q(cam_fecha_termino__gte = date.today())
            & Q(cam_creador = usu_id)

            
        ).distinct()

    data = {

        'campana': campana,
        'producto' : producto,
        'marca': marca,
        'color': color,
    }

    
    return render(request, 'app/marca_detalles.html', data)

def producto_detalles(request, slug_text):

    producto = Producto.objects.get(slug=slug_text)
    print(producto)

    context = {
        "producto" : producto,
        'color' : color,
    }

    return render(request, 'app/detalles_producto.html', context)

def buscar_tecnologia (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 1)).order_by('-id')
    marca = Marca.objects.filter(Q(mar_categoria__id__iexact = 1)).order_by('mar_creador')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
        'marca' : marca,
    }

    return render(request,'app/buscar_tecnologia.html',data)

def buscar_salud_y_belleza (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 2)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_salud_y_belleza.html',data)

def buscar_gastronomia (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 3)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_gastronomia.html',data)

def buscar_deportes_y_outdoor (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 4)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_deportes_y_outdoor.html',data)

def buscar_vestuario_y_calzado (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 5)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_vestuario_y_calzado.html',data)

def buscar_mascotas (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 6)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_mascotas.html',data)

def buscar_turismo_y_viajes (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 7)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_turismo_y_viajes.html',data)

def buscar_infantil (request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    campana = Campana.objects.filter(Q(cam_categoria__id__iexact = 8)).order_by('-id')
    #print(campana)
    busqueda = request.POST.get("buscar")

    if busqueda:

        campana = Campana.objects.filter(Q(cam_nombre__icontains = busqueda))

    data = {
        'campana' : campana,
        'color' : color,
    }

    return render(request,'app/buscar_infantil.html',data)

def mensajes(request): #esta parte está en blanco nicanor

    marca = Marca.objects.filter(mar_creador = request.user)
    marca = marca.first()

    campanas = Campana.objects.filter(cam_creador=request.user).values_list('id',flat=True)
    campanas = list(campanas)
    print("campanas: ", campanas)

    inter = Interaccion.objects.filter(int_cam_id__in = campanas).values_list('id',flat=True)
    inter = list(inter)

    print("inter: ", inter)

    today = datetime.now() # nuevo

    int_calificar = Int_Calificar.objects.filter(
        Q(intcal_fecha_int__lte = today) & Q(intcal_int_id__in = inter)
        ).order_by('-intcal_fecha_int').values_list('intcal_fecha_int',flat=True)
    
    int_compartir = Int_Compartir.objects.filter(
        Q(intcom_fecha_int__lte = today) & Q(intcom_int_id__in = inter)
        ).order_by('-intcom_fecha_int').values_list('intcom_fecha_int',flat=True)
    
    int_recomendar = Int_Recomendar.objects.filter(
        Q(intrec_fecha_int__lte = today) & Q(intrec_int_id__in = inter)
        ).order_by('-intrec_fecha_int').values_list('intrec_fecha_int',flat=True)

    int_calificar = list(int_calificar)
    cant_int_cal = len(int_calificar)

    int_compartir = list(int_compartir)
    cant_int_com = len(int_compartir)

    int_recomendar = list(int_recomendar)
    cant_int_rec = len(int_recomendar)

    print("int calificar: ", int_calificar)
    print("cant_int_cal: ", cant_int_cal)

    print("int compartir: ", int_compartir)
    print("cant_int_com: ", cant_int_com)

    print("int recomendar: ", int_recomendar)
    print("cant_int_rec: ", cant_int_rec)

    if cant_int_cal > 0:
        int_calificar = int_calificar[0]

    if cant_int_com > 0:
        int_compartir = int_compartir[0]
    
    if cant_int_rec > 0:
        int_recomendar = int_recomendar[0]

    data = {
        'marca': marca,
        'int_calificar': int_calificar,
        'cant_int_cal': cant_int_cal,
        'int_compartir': int_compartir,
        'cant_int_com': cant_int_com,
        'int_recomendar': int_recomendar,
        'cant_int_rec': cant_int_rec,

    }

    return render(request,'app/mensajes.html', data)

def perfil(request):

    color = Caracteristicas_Usuario.objects.filter(car_usu_usu_id = request.user.id)

    if color:
        color = color.first()
        color = color.car_usu_color_interfaz
    else:
        pass

    print(request.user.id)

    caracteristicas = get_object_or_404(Caracteristicas_Usuario, car_usu_usu_id=request.user.id)
    print("carecteristcas: ",caracteristicas)
    perfil = get_object_or_404(Perfil_Usuario, per_usu_usu_id = request.user.id )
    print("perfil: ", perfil)

    data = {

        'form2' : CaracteristicasForm(instance=caracteristicas),
        'form3' : Perfil_UsuarioForm(instance=perfil),
        'form4' : PasswordChangeForm(request.user),
        'color' : color,

    }
    
    if request.method == 'POST':

        formulario2 = CaracteristicasForm(data=request.POST, instance=caracteristicas)
        formulario3 = Perfil_UsuarioForm(data=request.POST, instance=perfil)
        formulario4 = PasswordChangeForm(user=request.user, data=request.POST)


        if formulario2.is_valid():

            print("se valida el formulario 2")

            datos = formulario2.save()
            messages.success(request, "Datos cambiados")

        else:

            data["form2"] = formulario2

        if formulario3.is_valid():

            

            datos_perfil = formulario3.save()
            messages.success(request, "avatar cambiados")

        else:
            
            data["form3"] = formulario3

        if formulario4.is_valid():

            formulario4.save()
            update_session_auth_hash(request, formulario4.user)
            #formulario2.save()
            
            send_mail(
                    "Uniperz - Cambio de contraseña de "+str(request.user),
                    "Usted ha cambiado de contraseña",
                    'no-reply@uniperz.com' ,
                    [request.user.email],
                    fail_silently=False,
                    )

            messages.success(request, "Contraseña modificada correctamente")

        else:

            print("no cambia la contra")
            data["form4"] = formulario4

            if formulario2.is_valid():

                print("se valida el formulario 2")

                datos = formulario2.save()
                messages.success(request, "Datos cambiados")


    return render(request,'app/perfil.html', data)

    

def export_to_xls(request, id):
    
    
    campana = get_object_or_404(Campana, id=id)
    #print(campana.cam_nombre)
    hora_actual = datetime.now()
    hora_formateada = hora_actual.strftime('%Y-%m-%d at %H.%M.%S')
    #print(hora_formateada)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Dashboard - '+campana.cam_nombre+' '+hora_formateada+'.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    

    instance_cal = Calificar.objects.get(cal_cam_id=campana.id)
    instance_com = Compartir.objects.get(com_cam_id=campana.id)
    instance_rec = Recomendar.objects.get(rec_cam_id=campana.id)

    #print("id campaña: ",id)

    if instance_cal.cal_booleano == True:
        ws1 = wb.add_sheet('Calificar')

    if instance_com.com_booleano == True:
        ws2 = wb.add_sheet('Compartir')

    if instance_rec.rec_booleano == True:
        ws3 = wb.add_sheet('Recomendar')

    

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.name = "Arial"

    columns = ['ID','Username', 'First name', 'Last name', 'Email address', ]
    columnas = ['Nombre','Fecha Inicio Interaccion','Medallas Conseguidas', 'Estado Interaccion', 'Rango Etario', 'Region' ]

    columns = columnas

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    font_style.name = "Arial"

    
    inter = Interaccion.objects.filter(int_cam_id = campana.id).values_list('int_usu_id','int_fecha','int_medallas_logradas','int_est_id')
    #inter = list(inter)
    #print(inter)
    lista_inter = []

    for i in inter:

        #print(i)
        tupla = i
        lista_tupla = list(tupla)

        id_usu = User.objects.get(id = lista_tupla[0]).id
        caracteristicas = Caracteristicas_Usuario.objects.get(car_usu_usu_id = id_usu)
        #print("caracteristica del usuario ", id_usu," : ",caracteristicas.car_usu_fecha_nacimiento , caracteristicas.car_usu_region)

        fecha_nacimiento = caracteristicas.car_usu_fecha_nacimiento
        edad = age(fecha_nacimiento.year, fecha_nacimiento.month, fecha_nacimiento.day)
        region = caracteristicas.car_usu_region

        if 15 <= edad <= 24:
            lista_tupla.append("15 a 24")
        elif 25 <= edad <= 34:
            lista_tupla.append("25 a 34")
        elif 35 <= edad <= 44:
            lista_tupla.append("35 a 44")
        elif 45 <= edad <= 54:
            lista_tupla.append("44 a 54")
        elif 55 <= edad <= 64:
            lista_tupla.append("55 a 64")
        elif 65 <= edad:
            lista_tupla.append("65 o más")
        elif 0 <= 14:
            lista_tupla.append("0 a 14")
        else:
            lista_tupla.append("error")

        #lista_tupla.append(edad)
        if region == 0:
            lista_tupla.append("Arica y Parinacota")
        elif region == 1:
            lista_tupla.append("Tarapacá")
        elif region == 2:
            lista_tupla.append("Antofagasta")
        elif region == 3:
            lista_tupla.append("Atacama")
        elif region == 4:
            lista_tupla.append("Coquimbo")
        elif region == 5:
            lista_tupla.append("Valparaiso")
        elif region == 6:
            lista_tupla.append("Region Metropolitana")
        elif region == 7:
            lista_tupla.append("O'Higgins")
        elif region == 8:
            lista_tupla.append("Maule")
        elif region == 9:
            lista_tupla.append("Ñuble")
        elif region == 10:
            lista_tupla.append("Biobío")
        elif region == 11:
            lista_tupla.append("Araucanía")
        elif region == 12:
            lista_tupla.append("Ríos")
        elif region == 13:
            lista_tupla.append("Lagos")
        elif region == 14:
            lista_tupla.append("Aysén")
        elif region == 15:
            lista_tupla.append("Magallanes y Antártica")

        
        #print(lista_tupla)


        #print(lista_tupla[1])
        lista_tupla[1] = str(lista_tupla[1])

        if lista_tupla[0] == User.objects.get(id = lista_tupla[0]).id :
            lista_tupla[0] = User.objects.get(id = lista_tupla[0]).first_name
            
        #print(lista_tupla[3])
        if lista_tupla[3] == 1:

            lista_tupla[3] = 'Activa'

        elif lista_tupla[3] == 2:

            lista_tupla[3] = 'Inactiva'
            
        elif lista_tupla[3] == 3:

            lista_tupla[3] = 'Finalizada'

        else:
            print("error")

        tupla = tuple(lista_tupla)
        #print("tupla ", tupla)
        lista_inter.append(tupla)
        #print(i)
        #print("funciona")

    #print(lista_inter)

    rows = User.objects.filter(groups__name="Usuario").values_list('id','username', 'first_name', 'last_name', 'email')
    rows = lista_inter
    #print(type(rows))
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def login_marcas(request):
    
    form = AuthenticationForm()

    data={
        'form': form,
    }

    if request.method == 'POST':
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                
                login(request, user)
                grupo = request.user.groups.all()

                if grupo: 
                
                    grupo = list(grupo)
                    grupo = str(grupo[0])

                    if grupo == 'Marca':

                        
                        return redirect(to="home")
                    
                    elif grupo == 'Usuario':
                        
                        return redirect(to="login_marcas")
                
            else:
                return redirect(to="login_marcas")
    
        else:
            pass

    

    return render(request,'registration/login_marcas.html',data)



def logout_marcas(request):

    #print(request.user.username, " vira")

    grupo = request.user.groups.all()
    if grupo: 
            
        grupo = list(grupo)
        grupo = str(grupo[0])
        print(grupo)
            
        if grupo == 'Marca':

            logout(request)
            return redirect(to="login_marcas")
            
        elif grupo == 'Usuario':
                
            logout(request)
            return redirect(to="login")

        else:
            pass
    else:
        pass
    
    logout(request)
    return redirect(to="login")

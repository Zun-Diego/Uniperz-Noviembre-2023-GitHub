from django.urls import path, include
from . import views
from .views import dashboard_campana, home, contacto, galeria, agregar_campana, desafio1, listar_campanas,\
 modificar_campana, eliminar_campana, registro, interacciones , CampanaViewset, caracteristicas, \
    politicas_privacidad, marcas, conf_marca, modificar_marca, marca_detalles, agregar_producto, \
        listar_productos, modificar_producto, eliminar_producto, inicio, graficos, buscar, \
            buscar_tecnologia, buscar_salud_y_belleza, buscar_gastronomia, buscar_deportes_y_outdoor, \
                buscar_vestuario_y_calzado, buscar_mascotas, buscar_turismo_y_viajes, \
                    buscar_infantil, mensajes, marca_cambiar_contrasena, perfil, interacciones_detalles, \
                        seleccionar_categorias, login_marcas ,logout_marcas


from django.contrib.auth.views import LogoutView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('campana',CampanaViewset)

urlpatterns = [
    path('', inicio, name="inicio"),
    path('testing/', home, name="home"),
    path('testing/interacciones/',interacciones,name="interacciones"),
    path('contacto/',contacto ,name="contacto"),
    path('galeria/', galeria,name="galeria"),
    path('agregar-campana/',agregar_campana, name="agregar_campana"),
    path('listar-campanas/',listar_campanas, name="listar_campanas"),
    path('modificar-campana/<id>/',modificar_campana, name="modificar_campana"),
    path('eliminar-campana/<id>/',eliminar_campana, name="eliminar_campana"),
    path('registro/',registro,name="registro"),
    path('api/',include(router.urls)),
    path('testing/interacciones_detalles/<id>', views.interacciones_detalles, name="interacciones_detalles"),
    path('testing/interacciones/<slug:slug_text>', views.detalles, name="interaccion"),
    path('testing/interacciones/<slug:slug_text>/desafio1', views.desafio1, name="desafio1"),
    path('testing/interacciones/<slug:slug_text>/desafio2', views.desafio2, name="desafio2"),
    path('testing/interacciones/<slug:slug_text>/desafio3', views.desafio3, name="desafio3"),
    path('testing/interacciones/<slug:slug_text>/desafio4', views.desafio4, name="desafio4"),
    path('create/', views.create, name='create'),
    path('vote/<poll_id>/', views.vote, name='vote'),
    path('results/<poll_id>/', views.results, name='results'),
    path('agregar-campana/preview', views.preview,name= "Previsualización Campaña"),
    path('caracteristicas/',caracteristicas,name="caracteristicas"),
    path('politicas_privacidad/',politicas_privacidad,name="politicas_privacidad"),
    path('dashboard-campana/<id>/', dashboard_campana, name = "dashboard_campana"),
    path('descargar-csv/<data>/',views.csvMaker, name= "csv_maker"),
    path('Avatar/',views.Avatar, name= "Avatar"),
    path('graficos/', views.graficos, name="graficos"),
    path('buscar/', views.buscar, name="buscar"),
    path('marcas/', views.marcas, name="marcas"),
    path('conf_marca/', views.conf_marca, name="conf_marca"),
    path('modificar_marca/<id>', views.modificar_marca, name="modificar_marca"),
    path('marca_cambiar_contrasena/<id>', views.marca_cambiar_contrasena, name="marca_cambiar_contrasena"),
    path('marca_detalles/<id>', views.marca_detalles, name="marca_detalles"),
    path('agregar-producto/',agregar_producto, name="agregar_producto"),
    path('listar-productos/',listar_productos, name="listar_productos"),
    path('modificar-producto/<id>/',modificar_producto, name="modificar_producto"),
    path('eliminar-producto/<id>/',eliminar_producto, name="eliminar_producto"),
    path('productos/<slug:slug_text>', views.producto_detalles, name="producto_detalles"),
    path('buscar/tecnologia', views.buscar_tecnologia, name="buscar_tecnologia"),
    path('buscar/salud_y_belleza', views.buscar_salud_y_belleza, name="buscar_salud_y_belleza"),
    path('buscar/gastronomia', views.buscar_gastronomia, name="buscar_gastronomia"),
    path('buscar/deportes_y_outdoor', views.buscar_deportes_y_outdoor, name="buscar_deportes_y_outdoor"),
    path('buscar/vestuario_y_calzado', views.buscar_vestuario_y_calzado, name="buscar_vestuario_y_calzado"),
    path('buscar/mascotas', views.buscar_mascotas, name="buscar_mascotas"),
    path('buscar/turismo_y_viajes', views.buscar_turismo_y_viajes, name="buscar_turismo_y_viajes"),
    path('buscar/infantil', views.buscar_infantil, name="buscar_infantil"),
    path('mensajes', views.mensajes, name="mensajes"),
    path('perfil', views.perfil, name="perfil"),
    path('export-to-xls/<id>', views.export_to_xls, name='export_to_xls'),
    path('seleccionar_categorias', views.seleccionar_categorias, name='seleccionar_categorias'),
    path('accounts/login_marcas/', views.login_marcas, name='login_marcas'),
    path('logout_marcas/', views.logout_marcas, name='logout_marcas'),

]


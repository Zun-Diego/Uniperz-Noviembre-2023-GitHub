from django.contrib import admin
from .models import Categoria, Campana, Contacto, Escala, Interaccion, Estado
from .forms import CampanaForm

# Register your models here.

class CampanaAdmin(admin.ModelAdmin):
    list_display = ["cam_nombre","cam_dias","cam_fecha_inicio","cam_fecha_termino"]
    form = CampanaForm

admin.site.register(Categoria)
admin.site.register(Escala)
admin.site.register(Campana, CampanaAdmin)
admin.site.register(Contacto)
admin.site.register(Interaccion)
admin.site.register(Estado)
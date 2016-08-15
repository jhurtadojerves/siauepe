from django.contrib import admin
from models import Representante


# Register your models here.

@admin.register(Representante)
class RepresentanteAdmin(admin.ModelAdmin):
	list_display = ('nombres', 'apellidos', )
	#list_editable = ('estado', 'tipo')


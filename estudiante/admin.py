# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Estudiante


from import_export import resources, fields
from import_export.admin import ImportMixin


class EstudianteResource(resources.ModelResource):
	class Meta:
		model = Estudiante
		fields = ('id', 'cedula', 'representante', 'apellido', 'nombre', 'estado' )
		import_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True


@admin.register(Estudiante)
class EstudianteAdmin(ImportMixin, admin.ModelAdmin):
	list_display = ['id','apellido','nombre', 'representante']
	ordering = ['id', 'apellido' ]
	search_fields = ['id','cedula', 'nombre', 'apellido', 'representante__nombres',]
	resource_class = EstudianteResource

# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Curso, Especialidad

from import_export import resources, fields
from import_export.admin import ImportMixin


class EspecialidadResource(resources.ModelResource):
	class Meta:
		model = Especialidad
		fields = ('id', 'nombre', )
		import_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True

class CursoResource(resources.ModelResource):
	class Meta:
		model = Curso
		fields = ('nombre', 'paralelo', )
		import_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
	list_display = ['nombre', 'paralelo', 'especialidad',]

@admin.register(Especialidad)
class EspecialidadAdmin(ImportMixin, admin.ModelAdmin):
	list_display = ['id','nombre',]
	class_resource = EspecialidadResource

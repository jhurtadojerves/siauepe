# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import CursoAsignatura
from import_export import resources, fields
from import_export.admin import ImportMixin

class CursoAsignaturaResource(resources.ModelResource):
	class Meta:
		model = CursoAsignatura
		fields = ('id', 'asignatura', 'curso', 'periodo', 'profesor', 'numero_horas', )
		import_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True

@admin.register(CursoAsignatura)
class CursoAsignaturaAdmin(ImportMixin, admin.ModelAdmin):
	list_display = ('asignatura', 'curso','periodo', 'profesor')
	class_resource = CursoAsignaturaResource
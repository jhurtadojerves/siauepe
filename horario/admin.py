# -*- coding: UTF-8 -*-
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportMixin
from models import Horario

# Register your models here.

class HorarioResource(resources.ModelResource):
	class Meta:
		model = Horario
		fields = ('hora', 'dia', 'cursoasignatura',)
		import_order = fields
		export_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True



@admin.register(Horario)
class HorarioAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['dia', 'hora', 'curso_asignado',]
    raw_id_fields = ('cursoasignatura',)
    class_resource = HorarioResource



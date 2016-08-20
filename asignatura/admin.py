# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Asignatura

from import_export import resources, fields
from import_export.admin import ImportMixin


class AsignaturaResource(resources.ModelResource):
	class Meta:
		model = Asignatura
		fields = ('id', 'nombre', )
		import_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True


@admin.register(Asignatura)
class AsignaturaAdmin(ImportMixin, admin.ModelAdmin):
	list_display = ['id','nombre',]
	search_fields = ['nombre']
	resource_class = AsignaturaResource
# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Periodo

from import_export import resources, fields
from import_export.admin import ImportExportMixin


class PeriodoResource(resources.ModelResource):
	class Meta:
		model = Periodo
		fields = ('id', 'nombre', 'activo', 'inicio', 'fin', )
		import_order = fields
		export_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True


@admin.register(Periodo)
class PeriodoAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['nombre', 'inicio', 'fin', 'activo']
	list_editable = ['activo',]
	resource_class = PeriodoResource
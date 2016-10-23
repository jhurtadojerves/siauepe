# -*- coding: utf-8 -*-
from django.contrib import admin

from import_export import resources, fields
from import_export.admin import ImportExportMixin
# Register your models here.

from models import Profesor

class ProfesorResource(resources.ModelResource):
	class Meta:
		model = Profesor
		fields = ('id','nombre_completo',)
		import_order = fields
		export_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True

@admin.register(Profesor)
class ProfesorAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ('id','nombre_completo',)
	resource_class = ProfesorResource
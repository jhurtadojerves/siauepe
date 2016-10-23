# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Curso, Especialidad

from import_export import resources, fields
from import_export.admin import ImportExportMixin


class EspecialidadResource(resources.ModelResource):
    class Meta:
        model = Especialidad
        fields = ('id', 'nombre', )
        import_order = fields
        export_order = fields
        IMPORT_EXPORT_SKIP_ADMIN_LOG = True

class CursoResource(resources.ModelResource):
    class Meta:
        model = Curso
        fields = ('nombre', 'paralelo', 'especialidad')
        export_order = fields
        import_order = fields
        IMPORT_EXPORT_SKIP_ADMIN_LOG = True

@admin.register(Curso)
class CursoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['nombre', 'paralelo', 'especialidad',]
    class_resource = CursoResource

@admin.register(Especialidad)
class EspecialidadAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','nombre',]
    class_resource = EspecialidadResource

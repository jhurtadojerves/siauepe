# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Curso, Especialidad

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'paralelo', 'especialidad',]

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre',]

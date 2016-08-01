# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import CursoAsignaturaEstudiante
@admin.register(CursoAsignaturaEstudiante)
class CursoAsignaturaEstudianteAdmin(admin.ModelAdmin):
    list_display = ('asignatura', 'estudiante',)
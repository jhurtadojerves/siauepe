# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import CursoAsignaturaEstudiante
@admin.register(CursoAsignaturaEstudiante)
class CursoAsignaturaEstudianteAdmin(admin.ModelAdmin):
	list_display = ('cursostr', 'asignaturastr', 'estudiante',)
	list_filter = ('cursostr', 'asignaturastr', 'estudiante',)
	search_fields = ('cursostr', 'asignaturastr', 'estudiante',)
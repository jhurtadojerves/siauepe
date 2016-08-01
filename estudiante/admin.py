# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Estudiante
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('cedula','nombre', 'apellido',)
    search_fields = ('cedula', 'nombre', 'apellido',)
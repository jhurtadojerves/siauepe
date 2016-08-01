# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import CursoAsignatura
@admin.register(CursoAsignatura)
class CursoAsignaturaAdmin(admin.ModelAdmin):
    list_display = ('asignatura', 'curso','periodo', 'profesor')
# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Horario

# Register your models here.

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['dia', 'hora', 'curso_asignado',]
    raw_id_fields = ('cursoasignatura',)



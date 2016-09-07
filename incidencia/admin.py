# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Incidencia


# Register your models here.

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
	list_display = ('id','fecha', 'ver_hora','estado', 'tipo')
	list_editable = ('estado', 'tipo')

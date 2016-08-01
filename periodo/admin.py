# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Periodo
@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'inicio', 'fin', 'activo']

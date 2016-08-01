# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Asignatura

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
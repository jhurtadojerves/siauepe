# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from models import Profesor
@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido',)
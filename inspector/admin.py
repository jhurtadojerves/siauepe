# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Inspector

# Register your models here.

@admin.register(Inspector)
class InspectorAdmin(admin.ModelAdmin):
    list_display = ('cedula',)


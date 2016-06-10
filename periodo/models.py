# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Periodo(models.Model):
    nombre = models.CharField(max_length=255)
    inicio = models.DateField(auto_now_add=True, blank=False)
    fin = models.DateField(auto_now_add=True, blank=False)
    activo = models.BooleanField(default=True)
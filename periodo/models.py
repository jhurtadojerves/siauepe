# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Periodo(models.Model):
    nombre = models.CharField(max_length=255)
    inicio = models.DateField(blank=False)
    fin = models.DateField(blank=False)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
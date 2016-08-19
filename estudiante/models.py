# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

from representante.models import Representante

# Create your models here.

class Estudiante(models.Model):
    id = models.IntegerField(primary_key=True)
    cedula = models.CharField(max_length=11, null=False,blank=False)
    nombre = models.CharField(max_length=32, null=False)
    apellido = models.CharField(max_length=32, null=False)
    representante = models.ForeignKey(Representante, blank=True, null=True)
    estado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre + " " + self.apellido
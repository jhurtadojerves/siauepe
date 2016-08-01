# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Estudiante(models.Model):
    cedula = models.CharField(max_length=11, unique=True, null=False,blank=False)
    nombre = models.CharField(max_length=32, null=False)
    apellido = models.CharField(max_length=32, null=False)

    def __unicode__(self):
        return self.nombre + " " + self.apellido
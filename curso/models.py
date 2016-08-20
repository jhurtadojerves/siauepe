# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Especialidad(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    paralelo = models.CharField(max_length=1, default='A')
    especialidad = models.ForeignKey(Especialidad)

    def __unicode__(self):
        return self.nombre
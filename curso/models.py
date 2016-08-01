# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Especialidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

class Curso(models.Model):
    nombre_opciones = (('1', 'Primero'),('2', 'Segundo'), ('3', 'Tercero'), ('4', 'Cuarto'),('5', 'Quinto'),('6', 'Sexto'),('7', 'Séptimo'),('8', 'Octavo'),('9', 'Noveno'))
    nombre = models.CharField(max_length=1, choices=nombre_opciones,default=1)
    paralelo = models.CharField(max_length=1, default='A')
    especialidad = models.ForeignKey(Especialidad)

    class Meta:
        unique_together = ('nombre', 'paralelo', 'especialidad', )

    def __unicode__(self):
        return self.nombre
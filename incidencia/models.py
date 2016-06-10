# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from django.db import models

from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from inspector.models import Inspector


# Create your models here.

class Incidencia(models.Model):

    asignaturaestudiante = models.ForeignKey(CursoAsignaturaEstudiante)

    fecha = models.DateField(auto_now_add=True, blank=False)

    estado_opciones = ((False, 'Injustificada'),(True, 'Justificada'))
    estado = models.BooleanField(choices=estado_opciones, default=False)

    tipo_opciones = (('F','Falta'), ('A', 'Atraso'))
    tipo = models.CharField(max_length=1,choices=tipo_opciones, default='A')

    revisado_por = models.ForeignKey(Inspector)
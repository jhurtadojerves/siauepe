# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from django.db import models

from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from cursoasignatura.models import CursoAsignatura
from inspector.models import Inspector
from horario.models import Horario
from django import forms
from datetime import timedelta, date, datetime


# Create your models here.

class Incidencia(models.Model):
	estado_opciones = ((False, 'Injustificada'),(True, 'Justificada'))
	tipo_opciones = (('F','Falta'), ('A', 'Atraso'))

	asignaturaestudiante = models.ForeignKey(CursoAsignaturaEstudiante, blank=True)
	fecha = models.DateField(blank=False)
	estado = models.BooleanField(choices=estado_opciones, default=False)
	tipo = models.CharField(max_length=1,choices=tipo_opciones, default='F')
	revisado_por = models.ForeignKey(Inspector, blank=True)

	class Meta:
		unique_together = ['asignaturaestudiante', 'fecha',]
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
	justificacion = models.CharField(max_length=1024, blank=True, null=True)
	asignaturaestudiante = models.ForeignKey(CursoAsignaturaEstudiante, blank=True)
	fecha = models.DateField(blank=False)
	estado = models.BooleanField(choices=estado_opciones, default=False)
	tipo = models.CharField(max_length=1,choices=tipo_opciones, default='F')
	revisado_por = models.ForeignKey(Inspector, blank=True)
	hora = models.ForeignKey(Horario)

	class Meta:
		unique_together = ['asignaturaestudiante', 'hora', 'fecha']

	def ver_hora(self):
		return self.hora.get_hora_display()

	def ver_estudiante(self):
		return self.asignaturaestudiante.estudiante.nombre_completo()

	def ver_asignatura(self):
		return self.asignaturaestudiante.asignatura.asignatura.nombre
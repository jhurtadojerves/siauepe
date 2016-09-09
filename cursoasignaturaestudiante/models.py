# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

from cursoasignatura.models import CursoAsignatura
from estudiante.models import Estudiante


# Create your models here.

class CursoAsignaturaEstudiante(models.Model):
	asignatura = models.ForeignKey(CursoAsignatura)
	estudiante = models.ForeignKey(Estudiante)

	def cursostr(self):
		return self.asignatura.curso.nombre

	def asignaturastr(self):
		return self.asignatura.asignatura.nombre

	def __unicode__(self):
		return self.asignatura.asignatura.nombre + " " + self.asignatura.curso.nombre
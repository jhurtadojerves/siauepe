# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

from cursoasignatura.models import CursoAsignatura


# Create your models here.

class Horario(models.Model):
	dias_opciones = (('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'),)
	dia = models.CharField(max_length=1, choices=dias_opciones, default='0')
	hora_opciones = (('1', '07:25 - 08:05'),
					 ('2', '08:05 - 08:45'),
					 ('3', '08:45 - 09:25'),
					 ('4', '09:25 - 10:05'),
					 ('5', '10:05 - 10:45'),
					 ('6', '10:45 - 11:25'),
					 ('7', '11:25 - 12:05'),
					 ('8', '12:05 - 12:45'),
					 ('9', '12:45 - 13:25'),
					 ('10', '13:25 - 12:05'),
					 )
	hora = models.CharField(max_length=1, choices=hora_opciones, default='1')
	cursoasignatura = models.ForeignKey(CursoAsignatura)

	class Meta:
		unique_together = ['dia', 'hora', 'cursoasignatura']


	def curso_asignado(self):
		return self.cursoasignatura.asignatura.nombre + " " + self.cursoasignatura.curso.nombre + " " + self.cursoasignatura.curso.paralelo + " " + self.cursoasignatura.curso.especialidad.nombre

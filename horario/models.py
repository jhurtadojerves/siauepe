# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

from cursoasignatura.models import CursoAsignatura

# Create your models here.

class Horario(models.Model):
    dias_opciones = (('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'),)
    dia = models.CharField(max_length=1, choices=dias_opciones, default='0')
    hora_opciones = (('1', 'Primera'),
                    ('2', 'Segunda'),
                    ('3', 'Tercera'),
                    ('4', 'Cuarta'),
                    ('5', 'Quinta'),
                    ('6', 'Sexta'),
                    ('7', 'Séptima'),
                    ('8', 'Octava'),
                    ('9', 'Novena'),
    )
    hora = models.CharField(max_length=1, choices=hora_opciones, default='1')
    cursoasignatura = models.ForeignKey(CursoAsignatura)

    def curso_asignado(self):
		return self.cursoasignatura.asignatura.nombre + " " +self.cursoasignatura.curso.nombre + " " + self.cursoasignatura.curso.paralelo + " " + self.cursoasignatura.curso.especialidad.nombre

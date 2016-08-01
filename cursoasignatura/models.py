# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

from asignatura.models import Asignatura
from curso.models import Curso
from periodo.models import Periodo
from profesor.models import Profesor

# Create your models here.

class CursoAsignatura(models.Model):
    asignatura=models.ForeignKey(Asignatura)
    curso=models.ForeignKey(Curso)
    periodo=models.ForeignKey(Periodo)
    profesor=models.ForeignKey(Profesor)
    numero_horas = models.IntegerField()

    class Meta:
        unique_together = ('asignatura', 'curso', 'periodo', 'profesor',)

    def __unicode__(self):
        return self.curso.nombre + " " +self.asignatura.nombre
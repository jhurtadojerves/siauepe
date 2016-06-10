# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

from cursoasignatura.models import CursoAsignatura
from estudiante.models import Estudiante

# Create your models here.

class CursoAsignaturaEstudiante(models.Model):
    asignatura=models.ForeignKey(CursoAsignatura)
    estudiante=models.ForeignKey(Estudiante)
# -*- coding: utf-8 -*-
__author__ = 'juliens'


from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django import forms
forms.DateInput.input_type="date"
forms.DateTimeInput.input_type="datetime-local"

from django.forms import ModelForm

from models import Incidencia
from incidencia.models import Incidencia
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from horario.models import Horario

from datetime import timedelta, date, datetime

class incidenciaForm(ModelForm):
    class Meta:
        model = Incidencia
        exclude = ['revisado_por', 'estado', 'asignaturaestudiante']
# -*- coding: utf-8 -*-
__author__ = 'juliens'

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django import forms

forms.DateInput.input_type = "date"
forms.DateTimeInput.input_type = "datetime-local"

from django.forms import ModelForm, Textarea

from models import Incidencia
from incidencia.models import Incidencia
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from horario.models import Horario

from datetime import timedelta, date, datetime
import re


class incidenciaForm(ModelForm):
	class Meta:
		model = Incidencia
		exclude = ['revisado_por', 'estado', 'asignaturaestudiante', 'cedula_representante', 'justificacion', 'hora',]


class EstudiantesForm(forms.Form):
	fecha = forms.DateField()
	options = (('F', 'Falta'), ('A', 'Atraso'))
	tipo = forms.ChoiceField(choices=options)
	estudiantes = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple, queryset=None)

	def __init__(self, query, *args, **kwargs):
		super(EstudiantesForm, self).__init__(*args, **kwargs)
		self.fields['estudiantes'].queryset = query
		self.fields['estudiantes'].empty_label = None
		self.fields['fecha'].widget.attrs.update({
			'class': 'form-control'
		})

class JustificarForm(ModelForm):
	class Meta:
		model = Incidencia
		fields = ['justificacion']
		widgets = {
			'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}

class IncidenciaDia(forms.Form):
	fecha = forms.DateField()	

class JustificarFechaForm(forms.Form):
	fecha_inicio = forms.DateField()
	fecha_fin = forms.DateField()
	justificacion = forms.CharField(widget=forms.Textarea)



	def clean_fecha_fin(self):
		fecha_inicio = self.cleaned_data['fecha_inicio']
		fecha_fin = self.cleaned_data['fecha_fin']
		if(fecha_fin>=fecha_inicio):
			return fecha_fin
		else:
			raise forms.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
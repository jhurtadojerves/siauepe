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
		exclude = ['revisado_por', 'estado', 'asignaturaestudiante', 'cedula_representante', 'justificacion']


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

	'''def clean_cedula_representante(self):
		"""
		Valída que sea Correcta la Cédula
		"""
		ced = self.cleaned_data['cedula_representante']
		regex = '[0-9]{9,9}[0-9]'
		if (re.match(regex, ced)):
			valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
			suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
			veri = 10 - (suma - (10 * (suma / 10)))
			if int(ced[9]) == int(str(veri)[-1:]):
				return ced
			else:
				raise forms.ValidationError('Ingrese una cédula válida')
		else:
			raise forms.ValidationError('Ingrese una cédula con el formato 1234567890')
	'''
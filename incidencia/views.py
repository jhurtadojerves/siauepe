# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json

from django.contrib.auth.models import User, Group

from models import Incidencia

from estudiante.models import Estudiante
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from periodo.models import Periodo
from cursoasignatura.models import CursoAsignatura
from inspector.models import Inspector
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from horario.models import Horario
from curso.models import Curso
from asignatura.models import Asignatura


from forms import incidenciaForm, EstudiantesForm, JustificarForm
from django import forms

# Create your views here.

from django.contrib.auth.decorators import login_required

import datetime, time

@login_required()
def home_incidencia(request):
	groups = request.user.groups.all()
	for g in groups:
		if g.name == 'Inspectores':
			return render(request, 'incidencia/home_incidencia.html', {}, context_instance=RequestContext(request))
	return render(request, 'nopermisos.html', {'error': 'Módulo de Incidencias'}, context_instance=RequestContext(request))

def busqueda(request):
	if request.is_ajax():
		estudiante = Estudiante.objects.filter(apellido__istartswith=request.GET['nombre']).values('nombre','apellido', 'id') | Estudiante.objects.filter(nombre__istartswith=request.GET['nombre']).values('nombre','apellido', 'id') | Estudiante.objects.filter(cedula__istartswith=request.GET['nombre']).values('nombre','apellido', 'id')
		return JsonResponse(list(estudiante), safe=False)
	return JsonResponse("Solo se permiten consultas mediante AJAX", safe=False)

@login_required()
def incidencia_buscar_estudiante(request):
	return render(request, 'incidencia/buscar_estudiante.html', {}, context_instance=RequestContext(request))

@login_required()
def incidencia_registrar_estudiante(request, id, id2):
	estudiante = get_object_or_404(Estudiante, id=id)
	asignaturaestudiante = get_object_or_404(CursoAsignaturaEstudiante, id = id2)
	asignatura = asignaturaestudiante.asignatura.asignatura
	p = Periodo.objects.get(activo = True)
	cA = CursoAsignatura.objects.filter(periodo=p)
	if request.method == 'POST':
		form = incidenciaForm(request.POST)
		if form.is_valid():
			inspector = get_object_or_404(Inspector, user = request.user)
			incidencia = form.save(commit=False)
			incidencia.revisado_por = inspector
			incidencia.asignaturaestudiante = asignaturaestudiante
			#horario = get_object_or_404(Horario, dia = incidencia.fecha.weekday())

			if not (Horario.objects.filter(dia = incidencia.fecha.weekday(), cursoasignatura = asignaturaestudiante.asignatura).exists()):
				return render(request, 'incidencia/registrar.html', {'form': form, 'estudiante': estudiante, 'asignatura':asignatura, 'horario': True},
							  context_instance=RequestContext(request))

			try:
				incidencia.save()
			except:
				return render(request, 'incidencia/registrar.html',
							  {'form': form, 'estudiante': estudiante, 'duplicado': True,
							   'asignatura': incidencia.asignaturaestudiante.asignatura.asignatura},
							  context_instance=RequestContext(request))

			return HttpResponseRedirect(reverse('incidencia_asignaturas_estudiante', args=(id))+"?incidencia=correcto",)
			#return render(request, 'index.html', {'form': form, 'estudiante': estudiante, 'ingresado': True}, context_instance=RequestContext(request))
	else:
		form = incidenciaForm()
	return render(request, 'incidencia/registrar.html', {'form': form, 'estudiante': estudiante, 'asignatura':asignatura}, context_instance=RequestContext(request))

@login_required()
def incidencia_asignaturas_estudiante(request, id):
	estudiante = get_object_or_404(Estudiante, id = id)
	periodo = get_object_or_404(Periodo, activo = True)
	asignaturas = CursoAsignaturaEstudiante.objects.filter(estudiante=estudiante, asignatura__periodo=periodo)
	return render(request, 'incidencia/estudiante_materias.html', {'asignaturas':asignaturas, 'estudiante':estudiante}, context_instance=RequestContext(request))


@login_required()
def incidencia_buscar_curso(request):
	periodo = get_object_or_404(Periodo, activo = True)
	cursoasignaturas = CursoAsignatura.objects.filter(periodo = periodo)

	aux = list()

	for ca in cursoasignaturas:
		aux.append(ca.curso.id)
	cursos =  Curso.objects.filter(id__in=aux).order_by('nombre',)

	return render(request, 'incidencia/cursos_periodo.html', {'cursos': cursos},
				  context_instance=RequestContext(request))

@login_required()
def incidencia_curso_materias(request, id):
	curso = get_object_or_404(Curso, id = id)
	periodo = get_object_or_404(Periodo, activo=True)
	asignaturasValues = CursoAsignatura.objects.filter(periodo=periodo, curso=curso).values('asignatura')
	asignaturas = Asignatura.objects.filter(id__in = asignaturasValues).order_by('nombre')
	return render(request, 'incidencia/cursos_periodo_materias.html', {'asignaturas': asignaturas},
				  context_instance=RequestContext(request))

@login_required()
def incidencia_curso_estudiantes(request, id_curso, id_asignatura):
	periodo = get_object_or_404(Periodo, activo = True)
	asignatura = get_object_or_404(Asignatura, id = id_asignatura)
	cursoasignatura = get_object_or_404(CursoAsignatura, asignatura = asignatura, periodo = periodo)
	cursoestudiantes = CursoAsignaturaEstudiante.objects.filter(asignatura=cursoasignatura).values('estudiante_id')
	estudiantes = Estudiante.objects.filter(id__in = cursoestudiantes)
	inspector = Inspector.objects.get(user=request.user)
	if request.method == 'POST':
		form = EstudiantesForm(query=estudiantes, data = request.POST)

		fechaString = request.POST.get('fecha')

		fecha = datetime.datetime.strptime(fechaString, '%Y-%m-%d').date()

		seleccionados = request.POST.getlist('estudiantes')
		tipo = request.POST.get('tipo')
		if (fechaString=='') or (len(seleccionados)==0):
			return render(request, 'incidencia/registrar.html', {'form': form, 'fecha':fecha,},
						  context_instance=RequestContext(request))

		if not (Horario.objects.filter(dia=fecha.weekday(),
									   cursoasignatura=cursoasignatura).exists()):
			return render(request, 'incidencia/registrar.html',
						  {'form': form, 'horario': True,
						   'asignatura': cursoasignatura.asignatura},
						  context_instance=RequestContext(request))


		stdSelected = Estudiante.objects.filter(id__in=seleccionados)

		crsEST = CursoAsignaturaEstudiante.objects.filter(asignatura=cursoasignatura, estudiante__in=stdSelected)

		for crsE in crsEST:
			if not(Incidencia.objects.filter(fecha = fecha, asignaturaestudiante=crsE).exists()):
				incidencia = Incidencia()
				incidencia.fecha = fecha
				incidencia.tipo = tipo
				incidencia.revisado_por = inspector
				incidencia.asignaturaestudiante = crsE
				incidencia.save()
		return HttpResponseRedirect(reverse('incidencia_curso_materias', args=(id_curso))+"?incidencia=correcto")
	else:
		form = EstudiantesForm(query=estudiantes)
	return render(request, 'incidencia/registrar.html', {'form': form,},
				  context_instance=RequestContext(request))


@login_required()
def incidencia_justificar(request):
	return render(request, 'incidencia/justificar/buscar_estudiante.html', {},
				  context_instance=RequestContext(request))

@login_required()
def incidencia_justificar_estudiante(request, id_estudiante):
	now = datetime.datetime.now()
	if(now.weekday()==0 or now.weekday()==6):
		dias = datetime.timedelta(days=3)
	elif (now.weekday()==1):
		dias = datetime.timedelta(days=4)
	else:
		dias = datetime.timedelta(days=2)

	estudiante = get_object_or_404(Estudiante, id = id_estudiante)
	incidencias = Incidencia.objects.filter(asignaturaestudiante__estudiante=estudiante, fecha__range=(now-dias, now), estado=False).order_by('asignaturaestudiante', 'fecha')

	return render(request, 'incidencia/justificar/incidencias.html', {'estudiante': estudiante, 'incidencias': incidencias},
				  context_instance=RequestContext(request))


@login_required()
def incidencia_justificar_estudiante_incidencia(request, id_estudiante, id_incidencia):
	now = datetime.datetime.now()
	if (now.weekday() == 0 or now.weekday() == 6):
		dias = datetime.timedelta(days=3)
	elif (now.weekday() == 1):
		dias = datetime.timedelta(days=4)
	else:
		dias = datetime.timedelta(days=2)

	incidencia = get_object_or_404(Incidencia, fecha__range=(now-dias, now), id=id_incidencia, estado=False)
	estudiante = incidencia.asignaturaestudiante.estudiante
	asignatura = incidencia.asignaturaestudiante.asignatura.asignatura

	if request.method=='POST':
		form = JustificarForm(request.POST, instance=incidencia)
		if form.is_valid():
			incidencia = form.save(commit=False)
			incidencia.estado = True
			incidencia.save()
			return HttpResponseRedirect(reverse('incidencia_justificar_estudiante', args=(estudiante.id,))+"?mensaje=correcto")
	else:
		form = JustificarForm(instance=incidencia)

	return render(request, 'incidencia/justificar/justificar.html',
				  {'form': form, 'estudiante': estudiante, 'asignatura': asignatura, 'incidencia':incidencia},
				  context_instance=RequestContext(request))





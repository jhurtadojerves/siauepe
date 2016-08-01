# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json

from django.contrib.auth.models import User, Group

from estudiante.models import Estudiante
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from periodo.models import Periodo
from cursoasignatura.models import CursoAsignatura
from inspector.models import Inspector
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from horario.models import Horario
from curso.models import Curso
from asignatura.models import Asignatura


from forms import incidenciaForm
from django import forms

# Create your views here.

from django.contrib.auth.decorators import login_required

@login_required()
def home_incidencia(request):
	groups = request.user.groups.all()
	for g in groups:
		if g.name == 'Inspectores':
			return render(request, 'incidencia/home_incidencia.html', {}, context_instance=RequestContext(request))
	return render(request, 'nopermisos.html', {'error': 'Módulo de Incidencias'}, context_instance=RequestContext(request))

def busqueda(request):
	if request.is_ajax():
		estudiante = Estudiante.objects.filter(apellido__startswith=request.GET['nombre']).values('nombre','apellido', 'id') | Estudiante.objects.filter(nombre__startswith=request.GET['nombre']).values('nombre','apellido', 'id') | Estudiante.objects.filter(cedula__startswith=request.GET['nombre']).values('nombre','apellido', 'id')
		return JsonResponse(list(estudiante), safe=False)
	return JsonResponse("Solo se permiten consultas mediante AJAX", safe=False)

@login_required()
def incidencia_buscar_estudiante(request):
	return render(request, 'incidencia/buscar_estudiante.html', {}, context_instance=RequestContext(request))

@login_required()
def incidencia_registrar_estudiante(request, id, id2):
	estudiante = get_object_or_404(Estudiante, id=id)
	asignaturaestudiante = get_object_or_404(CursoAsignaturaEstudiante, id = id2)
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
				return render(request, 'incidencia/registrar.html', {'form': form, 'estudiante': estudiante, 'horario': True, 'asignatura':incidencia.asignaturaestudiante.asignatura.asignatura},
							  context_instance=RequestContext(request))
			incidencia.save()
			#form = incidenciaForm()
			return HttpResponseRedirect(reverse('incidencia_asignaturas_estudiante', args=(id))+"?indicencia=correcto")
			return render(request, 'index.html', {'form': form, 'estudiante': estudiante, 'ingresado': True}, context_instance=RequestContext(request))
	else:
		form = incidenciaForm()
	return render(request, 'incidencia/registrar.html', {'form': form, 'estudiante': estudiante}, context_instance=RequestContext(request))

@login_required()
def incidencia_asignaturas_estudiante(request, id):
	estudiante = get_object_or_404(Estudiante, id = id)
	periodo = get_object_or_404(Periodo, activo = True)
	asignaturas = CursoAsignaturaEstudiante.objects.filter(estudiante=estudiante, asignatura__periodo=periodo)
	return render(request, 'incidencia/estudiante_materias.html', {'asignaturas':asignaturas}, context_instance=RequestContext(request))


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






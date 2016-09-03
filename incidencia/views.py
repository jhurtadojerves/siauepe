# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json

from django.contrib.auth.models import User, Group

from models import Incidencia

from estudiante.models import Estudiante, Matricula
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from periodo.models import Periodo
from cursoasignatura.models import CursoAsignatura
from inspector.models import Inspector
from cursoasignaturaestudiante.models import CursoAsignaturaEstudiante
from horario.models import Horario
from curso.models import Curso
from asignatura.models import Asignatura


import xlsxwriter
from xlsxwriter.utility import xl_range_abs




#####################################
#####################################
'''
////////////////////////////////////
///Librería para generar reportes///
////////////////////////////////////
'''
#####################################
#####################################

from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, A5, landscape, A6
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.lib.fonts import tt2ps


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
	curso = get_object_or_404(Curso, id = id_curso)
	cursoasignatura = get_object_or_404(CursoAsignatura, asignatura = asignatura, periodo = periodo, curso = curso)
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
	return render(request, 'incidencia/registrar_por_curso.html', {'form': form, 'curso':cursoasignatura},
				  context_instance=RequestContext(request))


@login_required()
def incidencia_justificar(request):
	return render(request, 'incidencia/justificar/buscar_estudiante.html', {},
				  context_instance=RequestContext(request))

@login_required()
def incidencia_justificar_estudiante(request, id_estudiante):
	now = datetime.datetime.now()
	if (now.weekday() == 0 or now.weekday()==1):
		dias = datetime.timedelta(days=4)
	elif (now.weekday() == 6):
		dias = datetime.timedelta(days=3)
	else:
		dias = datetime.timedelta(days=2)

	estudiante = get_object_or_404(Estudiante, id = id_estudiante)
	incidencias = Incidencia.objects.filter(asignaturaestudiante__estudiante=estudiante, fecha__range=(now-dias, now), estado=False).order_by('asignaturaestudiante', 'fecha')

	return render(request, 'incidencia/justificar/incidencias.html', {'estudiante': estudiante, 'incidencias': incidencias},
				  context_instance=RequestContext(request))


@login_required()
def incidencia_justificar_estudiante_incidencia(request, id_estudiante, id_incidencia):


	now = datetime.datetime.now()
	if (now.weekday() == 0 or now.weekday() == 1):
		dias = datetime.timedelta(days=4)
	elif (now.weekday() == 6):
		dias = datetime.timedelta(days=3)
	else:
		dias = datetime.timedelta(days=2)

	incidencia = get_object_or_404(Incidencia, fecha__range=(now-dias, now), id=id_incidencia, estado=False)
	estudiante = incidencia.asignaturaestudiante.estudiante
	asignatura = incidencia.asignaturaestudiante.asignatura.asignatura
	horario = Horario.objects.get(cursoasignatura=incidencia.asignaturaestudiante.asignatura, dia=incidencia.fecha.weekday())

	if request.method=='POST':
		form = JustificarForm(request.POST, instance=incidencia)
		if form.is_valid():
			incidencia = form.save(commit=False)
			incidencia.estado = True
			incidencia.save()

			estiloHoja = getSampleStyleSheet()
			cabecera = estiloHoja['Title']
			cabecera.pageBreakBefore = 0
			cabecera.keepWithNext = 0
			cabecera.textColor = colors.red
			estilo = estiloHoja['BodyText']

			salto = Spacer(0, 10)

			pagina = []

			pagina.append(salto)
			pagina.append(Paragraph("Unidad Educativa Particular Emanuel", cabecera))

			cabecera.textColor = colors.black
			pagina.append(Paragraph(""+"Justificación", cabecera))
			pagina.append(salto)
			pagina.append(salto)

			pagina.append(Paragraph("Estudiante: " + estudiante.nombre + " " + estudiante.apellido, estilo))
			pagina.append(Paragraph("Fecha: " + incidencia.fecha.strftime('%m/%d/%Y'), estilo))
			pagina.append(Paragraph("Hora: " + horario.get_hora_display(), estilo))
			pagina.append(Paragraph("Asignatura: " + asignatura.nombre, estilo))

			estilo.fontName = tt2ps('Times-Roman', 1, 0)

			pagina.append(Paragraph(""+"Justificación: ", estilo))
			estilo.fontName = tt2ps('Times-Roman', 0, 0)
			pagina.append(Paragraph("" + incidencia.justificacion, estilo))
			pagina.append(salto)
			pagina.append(salto)
			pagina.append(salto)
			pagina.append(salto)

			pagina.append(Paragraph(""+estudiante.representante.nombres_completos(), estilo))
			estilo.fontName = tt2ps('Times-Roman', 1, 0)
			pagina.append(Paragraph("REPRESENTANTE", estilo))
			pagina.append(salto)
			pagina.append(salto)
			pagina.append(salto)
			estilo.fontName = tt2ps('Times-Roman', 0, 0)
			pagina.append(Paragraph(incidencia.revisado_por.user.get_full_name(), estilo))
			estilo.fontName = tt2ps('Times-Roman', 1, 0)
			pagina.append(Paragraph("INSPECTOR", estilo))
			nombreArchivo= "justificante-"+incidencia.fecha.strftime('%m-%d-%Y')+".pdf"
			documento = SimpleDocTemplate(nombreArchivo, pagesize=A6,  showBoundary=1, displayDocTitle=1, leftMargin=2,
										  rightMargin=2, topMargin=2, bottomMargin=2, title="Justificante")

			documento.build(pagina)


			salida = open(nombreArchivo)
			response = HttpResponse(salida, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename='+nombreArchivo
			return response

			#return HttpResponseRedirect(reverse('incidencia_justificar_estudiante', args=(estudiante.id,))+"?mensaje=correcto")
	else:
		form = JustificarForm(instance=incidencia)

	return render(request, 'incidencia/justificar/justificar.html',
				  {'form': form, 'estudiante': estudiante, 'asignatura': asignatura, 'incidencia':incidencia},
				  context_instance=RequestContext(request))


@login_required()
def matricular(request):
	''
	periodo = get_object_or_404(Periodo, activo=True)
	matriculas = Matricula.objects.all()
	for m in matriculas:
		asignaturas = CursoAsignatura.objects.filter(curso=m.curso, periodo=periodo)
		for a in asignaturas:
			if not CursoAsignaturaEstudiante.objects.filter(asignatura = a, estudiante = m.estudiante).exists():
				cae = CursoAsignaturaEstudiante()
				cae.asignatura = a
				cae.estudiante = m.estudiante
				cae.save()

	return HttpResponse("Correcto, mostrar mensaje")

@login_required()
def reporte_index(request):
	return render(request, 'reportes/index.html', {},
				  context_instance=RequestContext(request))

@login_required()
def reporte_cursos(request):
	periodo = Periodo.objects.get(activo=True)
	cursoasignatura = CursoAsignatura.objects.filter(periodo = periodo).values_list('curso')
	cursos = Curso.objects.filter(id__in = cursoasignatura).order_by('especialidad')
	return render(request, 'reportes/ver_cursos.html', {'cursos':cursos},
				  context_instance=RequestContext(request))

@login_required()
def reporte_cursos_xls(request, curso):
	periodo = Periodo.objects.get(activo=True)
	curso = get_object_or_404(Curso, id = curso)

	cursoasignaturaestudiante = CursoAsignaturaEstudiante.objects.filter(asignatura__curso = curso, asignatura__periodo = periodo).order_by('asignatura')

	asignaturas = Asignatura.objects.filter(id__in = cursoasignaturaestudiante.values_list('asignatura__asignatura'))

	#estudiantes = Estudiante.objects.filter(id__in=cursoasignaturaestudiante.values_list('estudiante'))

	filename = 'reporte-curso.xls'

	wb = xlsxwriter.Workbook(filename)
	reporte = wb.add_worksheet('sheet1')
	reporte.set_column(0, 0, 25)
	reporte.set_column(1, 0, 25)
	reporte.set_column(2, 0, 25)
	reporte.set_column(3, 0, 25)
	reporte.set_column(4, 0, 25)
	num_format = wb.add_format({
		'num_format': '0',
		'align': 'right',
		'font_size': 12,

	})
	formato_negrita = wb.add_format({
		'bold': True,
		'align': 'center'
	})
	general_format = wb.add_format({
		'align': 'left',
		'font_size': 12,
	})

	filaInicio = 0
	reporte.merge_range(filaInicio, 0, filaInicio, 4, "UNIDAD EDUCATIVA PARTICULAR EMANUEL", formato_negrita)

	filaInicio+=2
	reporte.merge_range(filaInicio, 0, filaInicio, 4, "Reporte "+curso.nombre +" de "+ curso.especialidad.nombre + " paralelo "+curso.paralelo, formato_negrita)

	filaInicio += 2

	reporte.write(filaInicio, 1, "Horas Totales", formato_negrita)
	reporte.write(filaInicio, 2, u'Número de Estudiantes', formato_negrita)

	reporte.write(filaInicio, 3, "Cantidad de Faltas", formato_negrita)
	reporte.write(filaInicio, 4, "Cantidad de Atrasos", formato_negrita)

	filaInicio+=1

	for a in asignaturas:
		cursoasig = cursoasignaturaestudiante.filter(asignatura__asignatura=a)

		ca = CursoAsignatura.objects.get(asignatura = a, curso = curso, periodo = periodo)


		estudiantes = cursoasignaturaestudiante.filter(asignatura__asignatura=a).values_list('estudiante')

		faltas = Incidencia.objects.filter(asignaturaestudiante__in = cursoasig, tipo = "F")
		atrasos = Incidencia.objects.filter(asignaturaestudiante__in = cursoasig, tipo="A")
		reporte.write(filaInicio, 0, a.nombre, formato_negrita)

		reporte.write(filaInicio, 1, ca.numero_horas)
		reporte.write(filaInicio, 2, estudiantes.count())
		reporte.write(filaInicio, 3, faltas.count())
		reporte.write(filaInicio, 4, atrasos.count())
		filaInicio+=1
	'''
	chart = wb.add_chart({'type': 'pie'})
	chart.title_name = 'Temas'
	chart.width = reporte._size_col(0)
	values = '=%s!%s' % (reporte.name, xl_range_abs(inicio, 1, inicio + 2, 1))
	categories = '=%s!%s' % (reporte.name, xl_range_abs(inicio, 0, inicio + 2, 0))
	chart.add_series({'values': values, 'categories': categories, 'smooth': True})
	reporte.insert_chart(inicio + 4, 0, chart)

	chartBarras = wb.add_chart({'type': 'column'})
	chartBarras.title_name = 'Temas'
	chartBarras.width = reporte._size_col(0)
	chartBarras.add_series({'values': values, 'categories': categories, 'smooth': True})
	reporte.insert_chart(inicio + 4, 1, chartBarras)
	'''
	wb.close()
	output = open(filename)
	nombre = 'attachment; filename=' + filename
	#return HttpResponse(filename)
	response = HttpResponse(output, content_type="application/ms-excel")
	response['Content-Disposition'] = nombre
	return response


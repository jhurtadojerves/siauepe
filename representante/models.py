# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Representante(models.Model):
	codigorep = models.IntegerField(primary_key=True)
	nombres = models.CharField(max_length=100, blank=False, null=False)
	apellidos = models.CharField(max_length=100, blank=False, null=False)
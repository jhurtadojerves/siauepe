# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Asignatura(models.Model):
    nombre = models.CharField(max_length=255, null=False)

    def __unicode__(self):
        return self.nombre


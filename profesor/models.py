# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Profesor(models.Model):
    nombre_completo = models.CharField(max_length=128, null=False)

    def __unicode__(self):
        return self.nombre_completo
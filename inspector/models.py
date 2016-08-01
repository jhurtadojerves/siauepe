# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group

from django.db import models

# Create your models here.

class Inspector(models.Model):
    user = models.ForeignKey(User,unique=True)
    cedula = models.CharField(max_length=10, null=False, blank=False,unique=True)

    def clean(self):
        if(Group.objects.filter(name='Inspectores').exists()):
            grupo = Group.objects.get(name='Inspectores')
            self.user.groups.add(grupo)
        else:
            grupo = Group.objects.create(name="Inspectores")
            self.user.groups.add(grupo)
        return self
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Inspector(models.Model):
    user = models.ForeignKey(User,unique=True)

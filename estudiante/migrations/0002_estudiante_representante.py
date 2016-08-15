# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representante', '0001_initial'),
        ('estudiante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='representante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='representante.Representante'),
        ),
    ]

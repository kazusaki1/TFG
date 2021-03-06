# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-25 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abstractApp', '0003_auto_20170425_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuariorecompensa',
            options={'verbose_name': 'recompensa', 'verbose_name_plural': 'Añadir recompensa'},
        ),
        migrations.AddField(
            model_name='evento',
            name='event_fullDescription',
            field=models.CharField(default=1, max_length=250, verbose_name='Descripcion larga del evento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='image',
            field=models.ImageField(default=1, upload_to='', verbose_name='Imagen'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evento',
            name='event_description',
            field=models.CharField(max_length=50, verbose_name='Descripcion corta del evento'),
        ),
    ]

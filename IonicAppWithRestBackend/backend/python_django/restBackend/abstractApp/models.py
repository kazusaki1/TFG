from django.db import models
from datetime import datetime

class Image(models.Model):
    img = models.ImageField(upload_to = '')

class personas(models.Model):
	nombre = models.CharField(max_length=40)
	apellido = models.CharField(max_length=20)
	numero = models.CharField(max_length=10)

class eventos(models.Model):
	nombre = models.CharField(max_length=80)
	coorX = models.CharField(max_length=10)
	coorY = models.CharField(max_length=10)
	recompensa = models.CharField(max_length=70)
	disponible = models.BooleanField(True)
	start = models.DateField(default=datetime.now, blank=True)


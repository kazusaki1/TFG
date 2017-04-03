from django.db import models

class Image(models.Model):
    img = models.ImageField(upload_to = '')


class personas(models.Model):
	nombre = models.CharField(max_length=40)
	apellido = models.CharField(max_length=20)
	numero = models.CharField(max_length=10)


from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

tmp = ""

def fechaIniMayorActual(fechaIni):
    ini_date_formated = str(fechaIni).split("+")[0]
    date_today_formated = str(datetime.today()).split(".")[0]
    global tmp 
    tmp = ini_date_formated
    if ini_date_formated < date_today_formated:
        raise ValidationError(
            _('%(ini_date_formated)s is lower than current date'),
            params={'ini_date_formated': ini_date_formated},
        )

def fechaExpMayorIni(fechaExp):

    ini_date_formated = tmp
    exp_date_formated = str(fechaExp).split("+")[0]
    if ini_date_formated > exp_date_formated:
        raise ValidationError(
            _('%(exp_date_formated)s is lower than %(ini_date_formated)s'),
            params={
                'exp_date_formated': exp_date_formated,
                'ini_date_formated': ini_date_formated},
        )

def mayorZero(valor):

    if valor < 1:
        raise ValidationError(
            _('%(valor)s is not allowed'),
            params={
                'valor': valor},
        )

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)

    def returnEmailJSON(self):
        return {'email':str(self.user.email)}

class Imagen(models.Model):
    img = models.ImageField(upload_to = '',verbose_name='Imagen')

    class Meta:
        verbose_name_plural = "Imagenes"
    def __str__(self):
        return '['+str(self.id)+'] '+self.img.name


class Recompensa(models.Model):
    reward_name = models.CharField(max_length=70,verbose_name='Recompensa')

    class Meta:
        verbose_name_plural = "Crear recompensa"

    def __str__(self):
        return self.reward_name


class UsuarioRecompensa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')
    reward = models.ForeignKey(Recompensa, on_delete=models.CASCADE,verbose_name='Recompensa')
    key = models.CharField(validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')],max_length=12,verbose_name="Codigo",unique=True)



    class Meta:
        verbose_name_plural = "Añadir recompensa"
        verbose_name = "recompensa"

    def __str__(self):
        return ''


class Evento(models.Model):
    brand = models.CharField(max_length=50,verbose_name='Marca')
    event_name = models.CharField(max_length=20,verbose_name='Nombre del evento')
    event_description = models.CharField(max_length=50,verbose_name='Descripcion corta del evento')
    event_fullDescription = models.CharField(max_length=250,verbose_name='Descripcion larga del evento')
    event_direccion = models.CharField(max_length=50,verbose_name='Direccion')
    event_provincia = models.CharField(max_length=50,verbose_name='Provincia')
    event_pais = models.CharField(max_length=50,verbose_name='Pais')
    radio = models.FloatField(verbose_name='Radio')
    latitud = models.CharField(max_length=10,verbose_name='Latitud')
    longitud = models.CharField(max_length=10,verbose_name='Longitud')
    reward = models.OneToOneField(Recompensa,on_delete=models.CASCADE,unique=True,verbose_name='Recompensa')
    image = models.ImageField(upload_to = 'eventos/',verbose_name='Imagen')
    
    class Meta:
        verbose_name_plural = "Crear evento"

    def __str__(self):
        return '['+str(self.id)+'] '+self.brand+': '+self.event_name+' '+self.reward.reward_name


class EventoParada(models.Model):
    event = models.OneToOneField(Evento,on_delete=models.CASCADE,unique=True,verbose_name='Evento')
    cooldown = models.DurationField(verbose_name='Tiempo de espera')

    class Meta:
        verbose_name_plural = "Convertir evento en evento parada"

    def __str__(self):
        return '['+str(self.event.id)+'] '+self.event.brand+': '+self.event.event_name

    def returnJSON(self):
        cooldown_formated = str(self.cooldown)
        return {'id':str(self.event.id),'brand':self.event.brand,'event_name':self.event.event_name,'event_description':self.event.event_description, 'event_type':'parada','latitud':self.event.latitud,'longitud':self.event.longitud,'reward':self.event.reward.reward_name,'cooldown':cooldown_formated}

    def returnMap(self):
        cooldown_formated = str(self.cooldown)
        return {'id':str(self.event.id),'event_name':self.event.event_name.upper(),'event_type':'parada','latitud':self.event.latitud,'longitud':self.event.longitud,'reward':self.event.reward.reward_name,'cooldown':cooldown_formated}

    def getPosition(self):
        return {'latitud':self.event.latitud,'longitud':self.event.longitud}


class EventoLimitado(models.Model):
    event = models.OneToOneField(Evento,on_delete=models.CASCADE,unique=True,verbose_name='Evento')
    ini_date = models.DateTimeField(validators=[fechaIniMayorActual],verbose_name='Fecha de inicio')
    exp_date = models.DateTimeField(validators=[fechaExpMayorIni],verbose_name='Fecha de fin')

    class Meta:
        verbose_name_plural = "Convertir evento en evento limitado"

    def __str__(self):
        return '['+str(self.event.id)+'] '+self.event.brand+': '+self.event.event_name

    def returnJSON(self):
        ini_date_formated = str(self.ini_date).split("+")[0]
        exp_date_formated = str(self.exp_date).split("+")[0]
        return {'id':str(self.event.id),'brand':self.event.brand,'event_name':self.event.event_name,'event_description':self.event.event_description, 'event_fullDescription' : self.event.event_fullDescription, 'event_direccion' : self.event.event_direccion,'event_type':'limitado','latitud':self.event.latitud,'longitud':self.event.longitud,'reward':self.event.reward.reward_name,'ini_date':ini_date_formated,'exp_date':exp_date_formated}

    def returnMap(self):
        ini_date_formated = str(self.ini_date).split("+")[0]
        exp_date_formated = str(self.exp_date).split("+")[0]
        return {'id':str(self.event.id),'event_name':self.event.event_name.upper(),'event_type':'limitado','latitud':self.event.latitud,'longitud':self.event.longitud,'reward':self.event.reward.reward_name,'ini_date':ini_date_formated,'exp_date':exp_date_formated}

    def isAvaible(self):
        ini_date_formated = str(self.ini_date).split("+")[0]
        exp_date_formated = str(self.exp_date).split("+")[0]
        date_today_formated = str(datetime.today()).split(".")[0]
        if (date_today_formated > ini_date_formated) and (date_today_formated < exp_date_formated):
            return True
        return False

    def getPosition(self):
        return {'latitud':self.event.latitud,'longitud':self.event.longitud}


class UsuarioEventoParada(models.Model):    
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario')
    event = models.ForeignKey(EventoParada,on_delete=models.CASCADE,verbose_name='Evento')
    last_use = models.DateTimeField(verbose_name='Ultima vez usado')

    class Meta:
        unique_together = ["user", "event"]
        verbose_name_plural = "Inscribir usuario a evento parada"

    def __str__(self):
        return self.user.username+ ' - ['+str(self.event.event.id)+'] '+self.event.event.brand+': '+self.event.event.event_name

    def returnJSON(self):
        last_use_formated = str(self.last_use).split("+")[0]
        cooldown_formated = str(self.event.cooldown)
        return {'id':str(self.event.event.id),'brand':self.event.event.brand,'event_name':self.event.event.event_name,'event_description':self.event.event.event_description,'event_type':'parada','latitud':self.event.event.latitud,'longitud':self.event.event.longitud,'reward':self.event.event.reward.reward_name,'last_use':last_use_formated,'cooldown':cooldown_formated}

    def returnMap(self):
        last_use_formated = str(self.last_use).split("+")[0]
        cooldown_formated = str(self.event.cooldown)
        return {'id':str(self.event.event.id),'event_name':self.event.event.event_name.upper(),'event_type':'parada','latitud':self.event.event.latitud,'longitud':self.event.event.longitud,'reward':self.event.event.reward.reward_name,'last_use':last_use_formated,'cooldown':cooldown_formated}


    def isAvaible(self):
        up_time = self.last_use+timedelta(days=self.event.cooldown.days,seconds=self.event.cooldown.seconds)
        up_time_formated = str(up_time).split("+")[0]
        date_today_formated = str(datetime.today()).split(".")[0]
        if date_today_formated > up_time_formated:
            return True
        return False

    def getPosition(self):
        return {'latitud':self.event.event.latitud,'longitud':self.event.event.longitud}


class UsuarioEventoLimitado(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario')
    event = models.ForeignKey(EventoLimitado,on_delete=models.CASCADE,verbose_name='Evento')

    class Meta:
        unique_together = ["user", "event"]
        verbose_name_plural = "Inscribir usuario a evento limitado"

    def __str__(self):
        return self.user.username+ ' - ['+str(self.event.event.id)+'] '+self.event.event.brand+': '+self.event.event.event_name

from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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

class Imagen(models.Model):
    img = models.ImageField(upload_to = '',verbose_name='Imagen')

    class Meta:
        verbose_name_plural = "Imagenes"
    def __str__(self):
        return '['+str(self.id)+'] '+self.img.name

class Usuario(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='Usuario')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name_plural = "Modificar usuario"

    def __str__(self):
        return self.user_name.username

class Recompensa(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='Usuario')
    reward_name = models.CharField(max_length=70,verbose_name='Recompensa')
    quantity = models.PositiveIntegerField(validators=[mayorZero],default=1,verbose_name='Cantidad')

    def __str__(self):
        return ''


class Evento(models.Model):
    brand = models.CharField(max_length=50,verbose_name='Marca')
    event_name = models.CharField(max_length=20,verbose_name='Nombre del evento')
    event_description = models.CharField(max_length=150,verbose_name='Descripcion del evento')
    coorX = models.CharField(max_length=10,verbose_name='Coordenada X')
    coorY = models.CharField(max_length=10,verbose_name='Coordenada Y')
    reward = models.CharField(max_length=70,verbose_name='Recompensa')
    
    class Meta:
        verbose_name_plural = "Crear evento"

    def __str__(self):
        return '['+str(self.id)+'] '+self.brand+': '+self.event_name


class EventoParada(models.Model):
    event = models.OneToOneField(Evento,on_delete=models.CASCADE,unique=True,verbose_name='Evento')

    class Meta:
        verbose_name_plural = "Convertir evento en evento parada"

    def __str__(self):
        return '['+str(self.event.id)+'] '+self.event.brand+': '+self.event.event_name


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
        return {'id':str(self.event.id),'brand':self.event.brand,'event_name':self.event.event_name,'event_description':self.event.event_description,'coorX':self.event.coorX,'coorY':self.event.coorY,'reward':self.event.reward,'ini_date':ini_date_formated,'exp_date':exp_date_formated}
    
    def isAvaible(self):
        ini_date_formated = str(self.ini_date).split("+")[0]
        exp_date_formated = str(self.exp_date).split("+")[0]
        date_today_formated = str(datetime.today()).split(".")[0]
        if (date_today_formated > ini_date_formated) and (date_today_formated < exp_date_formated):
            return True
        return False


class UsuarioEventoParada(models.Model):    
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Usuario')
    event = models.ForeignKey(EventoParada,on_delete=models.CASCADE,verbose_name='Evento')
    last_use = models.DateTimeField(verbose_name='Ultima vez usado')
    cooldown = models.DurationField(verbose_name='Tiempo de espera')

    class Meta:
        unique_together = ["user", "event"]
        verbose_name_plural = "Inscribir usuario a evento parada"

    def __str__(self):
        return self.user.user_name.username+ ' - ['+str(self.event.event.id)+'] '+self.event.event.brand+': '+self.event.event.event_name

    def returnJSON(self):
        last_use_formated = str(self.last_use).split("+")[0]
        cooldown_formated = str(self.cooldown)
        return {'id':self.event.event.id,'brand':self.event.event.brand,'event_name':self.event.event.event_name,'event_description':self.event.event.event_description,'coorX':self.event.event.coorX,'coorY':self.event.event.coorY,'reward':self.event.event.reward,'last_use':last_use_formated,'cooldown':cooldown_formated}

    def isAvaible(self):
        up_time = self.last_use+timedelta(days=self.cooldown.days,seconds=self.cooldown.seconds)
        up_time_formated = str(up_time).split("+")[0]
        date_today_formated = str(datetime.today()).split(".")[0]
        if date_today_formated > up_time_formated:
            return True
        return False


class UsuarioEventoLimitado(models.Model):
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Usuario')
    event = models.ForeignKey(EventoLimitado,on_delete=models.CASCADE,verbose_name='Evento')

    class Meta:
        unique_together = ["user", "event"]
        verbose_name_plural = "Inscribir usuario a evento limitado"

    def __str__(self):
        return self.user.user_name.username+ ' - ['+str(self.event.event.id)+'] '+self.event.event.brand+': '+self.event.event.event_name

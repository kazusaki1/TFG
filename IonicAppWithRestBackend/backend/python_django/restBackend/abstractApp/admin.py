from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Imagen, Usuario, Evento, EventoParada, EventoLimitado, UsuarioEventoParada, UsuarioEventoLimitado, Recompensa

# Register your models here.
class ImagenInline(admin.StackedInline):
    model = Imagen
class UsuarioInline(admin.StackedInline):
    model = Usuario
class EventoInline(admin.StackedInline):
    model = Evento  
class EventoParadaInline(admin.StackedInline):
    model = EventoParada
class EventoLimitadoInline(admin.StackedInline):
    model = EventoLimitado
class UsuarioEventoParadaInline(admin.StackedInline):
    model = UsuarioEventoParada
class UsuarioEventoLimitadoInline(admin.StackedInline):
    model = UsuarioEventoLimitado
class RecompensaInline(admin.TabularInline):
    model = Recompensa
    extra = 0

    
# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ImagenInline, UsuarioInline, EventoInline, EventoParadaInline, EventoLimitadoInline, UsuarioEventoParadaInline, UsuarioEventoLimitadoInline, RecompensaInline,)

class ModificarEvento(admin.ModelAdmin):
	list_display = ('brand', 'event_name', 'event_description', 'coorX', 'coorY', 'reward')

class ModificarUsuario(admin.ModelAdmin):
	list_display = ('user_name', 'email')
	fieldsets = [
		(None, {'fields': ['user_name']}),
		(None, {'fields': ['email'],
                'description': "<h5>Email Format: user@gmail.com</h5>"}),
		]
	inlines=[RecompensaInline]

class ModificarEventoLimitado(admin.ModelAdmin):
	list_display = ('event','ini_date','exp_date')
	fieldsets = [
		(None, {'fields': ['event']}),
		(None, {'fields': ['ini_date'],
                'description': "<h5>Date Format: YYYY-M-D<br/>Time Format: H:M:S</h5>"}),
		(None, {'fields': ['exp_date'],
                'description': "<h5>Date Format: YYYY-M-D<br/>Time Format: H:M:S</h5>"}),
		]

class ModificarUsuarioEventoParada(admin.ModelAdmin):
	list_display = ('user','event','last_use','cooldown')
	fieldsets = [
		(None, {'fields': ['user','event']}),
		(None, {'fields': ['last_use'],
                'description': "<h5>Date Format: YYYY-M-D<br/>Time Format: H:M:S</h5>"}),
		(None, {'fields': ['cooldown'],
                'description': "<h5>Cooldown Format: D H:M:S</h5>"}),
		]

class ModificarUsuarioEventoLimitado(admin.ModelAdmin):
	list_display = ('user','event')

class ModificarImagen(admin.ModelAdmin):
	list_display = ('id', 'img')

admin.site.register(Imagen,ModificarImagen)
admin.site.register(Usuario,ModificarUsuario)
admin.site.register(Evento,ModificarEvento)
admin.site.register(EventoParada)
admin.site.register(EventoLimitado,ModificarEventoLimitado)
admin.site.register(UsuarioEventoParada,ModificarUsuarioEventoParada)
admin.site.register(UsuarioEventoLimitado,ModificarUsuarioEventoLimitado)
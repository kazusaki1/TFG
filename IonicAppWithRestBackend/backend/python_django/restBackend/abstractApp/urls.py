from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'perfil/', views.perfil, name='perfil'),
    url(r'lista/', views.lista, name='lista'),
    url(r'^lista/(?P<type>.*)$', views.listaFiltrada, name='listaFiltrada'),
    url(r'evento/(?P<id>.*)/',views.evento, name='evento'),
    url(r'eventoparada/$',views.eventoParada, name='eventoParada'),
	url(r'mapa/(?P<myPosition>.*)$',views.mapa, name='mapa'),
	url(r'^sendImage/$', views.sendImage, name='sendImage'),
	url(r'login/',views.login, name='login'),
]

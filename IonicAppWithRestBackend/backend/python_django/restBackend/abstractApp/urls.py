from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'perfil/', views.perfil, name='perfil'),
    url(r'lista/', views.lista, name='lista'),
    url(r'listaFiltrada', views.listaFiltrada, name='listaFiltrada'),
    url(r'evento/(?P<id>.*)/',views.evento, name='evento'),
    url(r'eventoParada/',views.eventoParada, name='eventoParada'),
	url(r'mapa/(?P<info>.*)$',views.mapa, name='mapa'),
	url(r'^sendImage/$', views.sendImage, name='sendImage'),
	url(r'login/',views.login, name='login'),
	url(r'register/',views.register, name='register'),
	url(r'checkLogin/',views.checkLogin, name='checkLogin'),
]

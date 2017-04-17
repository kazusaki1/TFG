from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'smugglers/', views.smugglers, name='smugglers'),
    url(r'personas/', views.personas, name='personas'),
    url(r'lista/', views.lista, name='lista'),
    url(r'evento/(?P<id>.*)/',views.evento, name='evento'),
	url(r'texto/(?P<texto>.*)/',views.processFile, name='processFile'),
	url(r'^sendImage/$', views.sendImage, name='sendImage'),
]

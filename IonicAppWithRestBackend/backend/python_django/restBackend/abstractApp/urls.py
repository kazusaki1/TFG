from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'smugglers/', views.smugglers, name='smugglers'),
    url(r'personas/', views.personas, name='personas'),
    url(r'smuggler/(?P<id>[0-9]+)/',views.details, name='details'),
	url(r'texto/(?P<texto>.*)/',views.ProcessFile, name='ProcessFile'),
	url(r'^sendImage/$', views.sendImage, name='sendImage'),
]

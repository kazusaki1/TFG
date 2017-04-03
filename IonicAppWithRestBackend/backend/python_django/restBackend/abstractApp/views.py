from django.shortcuts import render,HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.core.files.base import ContentFile
import uuid
from .models import Image
import json
# Create your views here.
def index(request):
    return HttpResponse("Chewie we're home")

def smugglers(request):
	hondo = {'name':'Hondo','lastname': 'Ohnaka', 'id':1}
	han = {'name':'Han','lastname':'Solo','id':2}
	prueba = {'name':'Esto es','lastname':'una prueba','id':3}
	smugglers = [hondo,han,prueba]
	data = json.dumps(smugglers)
	print(request)
	return HttpResponse(data)


def details(request,id):
    species = 'Human'
    if id == '1':
        species = 'Weequay'
    return HttpResponse(species)

def ProcessFile(request,texto):
	print(request)
	print(texto)
	return HttpResponse(texto)
	
@csrf_exempt 	

def sendImage(request):
	image_data = str(request.body,"UTF-8")
	format, imgstr = image_data.split(';base64,') 
	ext = format.split('/')[-1] 
	image_name = str(uuid.uuid4()) + ".jpeg"
	x = Image()
	x.img = ContentFile(b64decode(imgstr), name=image_name)
	x.save()

	return HttpResponse(request)
	
	
def personas(request):
	paco = {'nombre':'Paco','apellido':'Bombo','numero':1}
	benito = {'nombre':'Benito','apellido':'Camela','numero':69}
	amparo = {'nombre':'Amparo','apellido':'PoZi','numero':5}
	personas = [paco, benito, amparo]

	datos = json.dumps(personas)
	print(request)
	return HttpResponse(datos)
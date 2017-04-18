from django.shortcuts import render,HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.core.files.base import ContentFile
import uuid
from .models import Imagen, Usuario, Evento, EventoParada, EventoLimitado, UsuarioEventoParada, UsuarioEventoLimitado
import json
from .Lasagne.recognizeImage import main
from datetime import datetime

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

def processFile(request,texto):
	print(request)
	print(texto)
	return HttpResponse(texto)
	
@csrf_exempt
def sendImage(request):
	image_data = str(request.body,"UTF-8")
	format, imgstr = image_data.split(';base64,') 
	ext = format.split('/')[-1] 
	image_name = str(uuid.uuid4()) + ".jpeg"
	x = Imagen()
	x.img = ContentFile(b64decode(imgstr), name=image_name)
	x.save()
	label = main(image_name)
	print(label)
	
	return HttpResponse(label)
	
	
def personas(request):
	paco = {'nombre':'Paco','apellido':'Bombo','numero':1}
	benito = {'nombre':'Benito','apellido':'Camela','numero':69}
	amparo = {'nombre':'Amparo','apellido':'PoZi','numero':5}
	personas = [paco, benito, amparo]

	datos = json.dumps(personas)
	print(request)
	return HttpResponse(datos)

def lista(request):

	# Guardar evento en base de datos
	#today = datetime.today()
	#today = str(today).split(".")[0]
	#eventos = Eventos(label='damm',nombre='Busca tabletas!',coorX='43',coorY='12',recompensa='2x1 BK',disponible='True',start=today).save()
	eventos = EventoLimitado.objects.all()
	prepareToSend = []
	for evento in eventos:
		prepareToSend.append(evento.returnJSON())
	
	
	datos = json.dumps(prepareToSend)

	return HttpResponse(datos)
	
def evento(request,id):

    print(id)
    evento = UsuarioEventoParada.objects.get(id=id)
    prepareToSend = []
    prepareToSend.append(evento.returnJSON())
    datos = json.dumps(prepareToSend)
    print(datos)
    
    return HttpResponse(datos)
	

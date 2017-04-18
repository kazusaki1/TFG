from django.shortcuts import render,HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.core.files.base import ContentFile
import uuid
from .models import Imagen, Usuario, Evento, EventoParada, EventoLimitado, UsuarioEventoParada, UsuarioEventoLimitado
import json
from .Lasagne.recognizeImage import main
from datetime import datetime
from math import sqrt

# Create your views here.
def index(request):
    return HttpResponse()

def perfil(request):
	return HttpResponse()

def mapa(request):
	eventosParada = EventoParada.objects.all()
	eventosLimitados = EventoLimitado.objects.all()
	prepareToSend = []
	coord = []
	myLocation = {'x':'41.411321','y':'2.175568'}
	for evento in eventosParada:
		distance = sqrt((float(evento.getCoord()['x']) - 41.411321)**2 + (float(evento.getCoord()['y']) - 2.175568)**2)
		if distance < 0.01:
			prepareToSend.append(evento.returnJSON())
	for evento in eventosLimitados:
		distance = sqrt((float(evento.getCoord()['x']) - 41.411321)**2 + (float(evento.getCoord()['y']) - 2.175568)**2)
		if distance < 0.01:
			prepareToSend.append(evento.returnJSON())
	#print(coord)
	#print(get_ordered_list(coord,41.411321,2.175568));
	#print(sqrt((float(coord[1]['x']) - 41.411321)**2 + (float(coord[1]['y']) - 2.175568)**2))
	
	datos = json.dumps(prepareToSend)
	print(datos)
	return HttpResponse(datos)
	
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
    evento = EventoLimitado.objects.get(event_id=id)
    prepareToSend = []
    prepareToSend.append(evento.returnJSON())
    datos = json.dumps(prepareToSend)
    print(datos)
    
    return HttpResponse(datos)
	

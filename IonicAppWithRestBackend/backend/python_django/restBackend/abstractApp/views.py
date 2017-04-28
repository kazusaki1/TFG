from django.shortcuts import render,HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.core.files.base import ContentFile
import uuid
from .models import Imagen, Evento, EventoParada, EventoLimitado, UsuarioEventoParada, UsuarioEventoLimitado, Recompensa, UsuarioRecompensa, Usuario
from django.contrib.auth.models import User
import json
from .Lasagne.recognizeImage import main
from datetime import datetime
from math import sqrt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from uuid import uuid4

# Create your views here.
def index(request):
    return HttpResponse()

def perfil(request):
	return HttpResponse()

def mapa(request, info):

	prepareToSend = []
	position = []

	# Get events
	eventosParada = EventoParada.objects.all()
	eventosLimitados = EventoLimitado.objects.all()

	# User
	user = info[info.find('usr=')+4:info.find('&lat=')]
	user = User.objects.get(username=user)
	user_id = user.id

	# My current position
	latitud = float(info[info.find('&lat=')+5:info.find('&lng=')])
	longitud = float(info[info.find('&lng=')+5:])

	# Stop events
	for evento in eventosParada:
		distance = sqrt((float(evento.getPosition()['latitud']) - latitud)**2 + (float(evento.getPosition()['longitud']) - longitud)**2)
		# Save nearby events
		if distance < 0.01: # ~1km	
			isVisited = UsuarioEventoParada.objects.filter(user_id=user_id,event_id=evento.id) # MODIFICAR USER_ID=1 POR USER_ID=REQUEST.USER.ID !!
			if isVisited:
				if not isVisited[0].isAvaible():
					prepareToSend.append(isVisited[0].returnMap())
				else:
					prepareToSend.append(evento.returnMap())
			else:
				prepareToSend.append(evento.returnMap())


	# Limited events
	for evento in eventosLimitados:
		distance = sqrt((float(evento.getPosition()['latitud']) - latitud)**2 + (float(evento.getPosition()['longitud']) - longitud)**2)
		# Save nearby events
		if distance < 0.01: # ~1km
			isVisited = UsuarioEventoLimitado.objects.filter(user_id=user_id,event_id=evento.id) # MODIFICAR USER_ID=1 POR USER_ID=REQUEST.USER.ID !!
			if not isVisited:			
				prepareToSend.append(evento.returnMap())

	#print(position)
	#print(get_ordered_list(position,41.411321,2.175568));
	#print(sqrt((float(position[1]['x']) - 41.411321)**2 + (float(position[1]['y']) - 2.175568)**2))
	
	datos = json.dumps(prepareToSend)
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
	#eventos = Eventos(label='damm',nombre='Busca tabletas!',latitud='43',longitud='12',recompensa='2x1 BK',disponible='True',start=today).save()
	eventos = EventoLimitado.objects.all()
	prepareToSend = []
	for evento in eventos:
		prepareToSend.append(evento.returnJSON())
	
	datos = json.dumps(prepareToSend)
	return HttpResponse(datos)

def listaFiltrada(request,type):

	if type[0] == "f":
		# FILTRAR POR FECHA
		eventos = EventoLimitado.objects.all()

	elif type[0] == "p":
		# FILTRAR POR PROVINCIA
		eventos = EventoLimitado.objects.all()

	

	prepareToSend = []
	for evento in eventos:
		prepareToSend.append(evento.returnJSON())
	
	datos = json.dumps(prepareToSend)
	return HttpResponse(datos)
	
def evento(request,id):

    evento = EventoLimitado.objects.get(event_id=id)
    prepareToSend = []
    prepareToSend.append(evento.returnJSON())
    datos = json.dumps(prepareToSend)
    
    return HttpResponse(datos)


@csrf_exempt
def eventoParada(request):

	evento = EventoParada.objects.get(event_id=request.body)
	eventoParada = UsuarioEventoParada.objects.get(event_id=evento.id,user_id=1) # MODIFICAR USER_ID=1 POR USER_ID=REQUEST.USER.ID !!

	reward = Evento.objects.get(id=request.body)
	key = generarKey()
	UsuarioRecompensa(key=key,reward_id=reward.reward_id,user_id=1).save()# MODIFICAR USER_ID=1 POR USER_ID=REQUEST.USER.ID !!

	date_today_formated = str(datetime.today()).split(".")[0]
	eventoParada.last_use=date_today_formated
	eventoParada.save()
	prepareToSend = []
	prepareToSend.append(eventoParada.returnJSON())
	datos = json.dumps(prepareToSend)
    
	return HttpResponse(datos)

def generarKey():

	try:
		key = UsuarioRecompensa.objects.latest('key').key
		key = str(int(key)+1).zfill(12)
	except UsuarioRecompensa.DoesNotExist:
		key = "000000000000"
	
	return key

@csrf_exempt
def login(request):
	prepareToSend = []
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser:
		prepareToSend.append({'access':'false'})
		datos = json.dumps(prepareToSend)
		return HttpResponse(datos)
	user = authenticate(username=infoUser['username'], password=infoUser['password'])
	if(user):
		token = uuid4()
		try:
			userToken = Usuario.objects.get(user_id=user.id)
			userToken.token = str(token)
			userToken.save()
		except Usuario.DoesNotExist:
			Usuario(user_id=user.id,token=str(token)).save()

		prepareToSend.append({'access':'true','token':str(token)})

	else:
		prepareToSend.append({'access':'false'})
	datos = json.dumps(prepareToSend)

	return HttpResponse(datos)

@csrf_exempt
def checkLogin(request):
	
	datos = "false"
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser or 'username' not in infoUser or 'token' not in infoUser:
		return HttpResponse(datos)
	datos = isTokenCorrect(infoUser['username'],infoUser['token'])

	return HttpResponse(datos)


def isTokenCorrect(user,token):
	try:
		user = User.objects.get(username=user)
		userToken = Usuario.objects.get(user_id=user.id)
		if(userToken.token == token):
			return "true"
		else:
			return "false"
	except User.DoesNotExist:
		return "false"
	except Usuario.DoesNotExist:
		return "false"


@csrf_exempt
def register(request):
	datos = "false"
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser or 'username' not in infoUser or 'password' not in infoUser or 'confirmPassword' not in infoUser or 'email' not in infoUser or infoUser['password'] != infoUser['confirmPassword']:
		return HttpResponse(datos)
	
	try:
		User.objects.create_user(username=infoUser['username'], password=infoUser['password'], email=infoUser['email']).save()
		datos = "true"
	except:
		datos = "false"

	return HttpResponse(datos)

	

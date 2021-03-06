from django.shortcuts import render,HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.core.files.base import ContentFile
import uuid
from .models import Imagen, Evento, EventoParada, EventoLimitado, UsuarioEventoParada, UsuarioEventoLimitado, Recompensa, UsuarioRecompensa, Usuario
from django.contrib.auth.models import User
import json
from .Lasagne.recognizeImage import main
from .Lasagne.loadModel import loadModel
from datetime import datetime
from math import sqrt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.core import serializers
import PIL
from PIL import Image
from scipy import misc
import os

test_net = loadModel()

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
	if user != "undefined":
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
	
	else:
		prepareToSend.append("error")

	datos = json.dumps(prepareToSend)
	return HttpResponse(datos)

from io import BytesIO
import base64

@csrf_exempt
def sendImage(request):
	info = json.loads(str(request.body,"UTF-8"))	
	success = "false"
	if not info or 'username' not in info or 'token' not in info or 'img' not in info or 'brand' not in info or 'event_id' not in info:
		return HttpResponse(success)

	if isTokenCorrect(info['username'],info['token']) == "false":
		return HttpResponse(success)

	image_data = info['img']
	brand = info['brand']

	format, imgstr = image_data.split(';base64,') 
	ext = format.split('/')[-1] 
	image_name = str(uuid.uuid4()) + '.' + ext

	x = Imagen()
	x.img = ContentFile(b64decode(imgstr), name=image_name)
	x.save()

	success = main(image_name, test_net, brand)

	if success == "true":
		try:
			user = User.objects.get(username=info['username'])
			evento = EventoLimitado.objects.get(event_id=info['event_id'])
			UsuarioEventoLimitado(event_id=evento.id,user_id=user.id).save()
			#crear key etc
			reward = Evento.objects.get(id=info['event_id'])
			key = generarKey()
			UsuarioRecompensa(key=key,reward_id=reward.reward_id,user_id=user.id).save()
		except User.DoesNotExist:
			success = "false"
		except EventoLimitado.DoesNotExist:
			success = "false"
		except:
			success = "false"


	print(success)

	
	return HttpResponse(success)

@csrf_exempt
def lista(request):
	user = str(request.body,"UTF-8")
	try:
		user = User.objects.get(username=user)	
		eventos = EventoLimitado.objects.all()
		prepareToSend = []
		for evento in eventos:
			if not UsuarioEventoLimitado.objects.filter(event_id=evento.id,user_id=user.id):
				prepareToSend.append(evento.returnJSON())
		datos = json.dumps(prepareToSend)
	except:
		datos = "ERROR Lista"
	return HttpResponse(datos)

@csrf_exempt
def listaFiltrada(request):

	info = json.loads(str(request.body,"UTF-8"))
	if not info or 'username' not in info or 'type' not in info or 'info' not in info:
		return HttpResponse("ERROR")
	try:
		if info['type'] == "f":
			# FILTRAR POR FECHA
			eventos = EventoLimitado.objects.all()

		elif info['type'] == "l":
			# FILTRAR POR LOCALIDAD
			prov = info['info'][0]
			
			eventos = Evento.objects.all().filter(event_provincia=prov)

		
		user = User.objects.get(username=info['username'])
		prepareToSend = []
		for evento in eventos:
			if EventoLimitado.objects.filter(event_id=evento.id):
				event = EventoLimitado.objects.filter(event_id=evento.id)
				#print(user.id)
				if not UsuarioEventoLimitado.objects.filter(event_id=event[0].event_id,user_id=user.id):
					prepareToSend.append(event[0].returnJSON())
		
		print(prepareToSend)
		datos = json.dumps(prepareToSend)
		return HttpResponse(datos)
	except:
		datos = "error"

	return HttpResponse(datos)
	

def evento(request,id):

    evento = EventoLimitado.objects.get(event_id=id)
    prepareToSend = []
    prepareToSend.append(evento.returnJSON())
    datos = json.dumps(prepareToSend)
    print(datos)
    return HttpResponse(datos)


@csrf_exempt
def eventoParada(request):

	info = json.loads(str(request.body,"UTF-8"))	
	if info and 'username' in info and 'event_id' in info:
		user = User.objects.get(username=info['username'])
		evento = EventoParada.objects.get(event_id=info['event_id'])
		try:
			eventoParada = UsuarioEventoParada.objects.get(event_id=evento.id,user_id=user.id)
		except UsuarioEventoParada.DoesNotExist:
			eventoParada = UsuarioEventoParada(event_id=evento.id,user_id=user.id)

		date_today_formated = str(datetime.today()).split(".")[0]
		eventoParada.last_use=date_today_formated
		eventoParada.save()

		reward = Evento.objects.get(id=info['event_id'])
		key = generarKey()
		UsuarioRecompensa(key=key,reward_id=reward.reward_id,user_id=user.id).save()

    
	return HttpResponse()

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

	print("TOKEN")
	datos = "false"
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser or 'username' not in infoUser or 'token' not in infoUser:
		return HttpResponse(datos)
	datos = isTokenCorrect(infoUser['username'],infoUser['token'])
	print("TOKEN: "+datos)

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

@csrf_exempt
def ourPerfil(request):
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser or 'name' not in infoUser:
		return HttpResponse('false')

	try:
		info = User.objects.get(username=infoUser['name'])
		prepareToSend = []
		prepareToSend.append(info.email)
		prepareToSend.append(info.username)
		datos = json.dumps(prepareToSend)
		return HttpResponse(datos)
	except:
		return HttpResponse('false')

@csrf_exempt
def actualizarPerfil(request):
	datos = "false"
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser:
		datos = "NOTINFO"
		return HttpResponse(datos)
	
	if 'email' in infoUser and 'password' not in infoUser and 'confirmPassword' not in infoUser:
		#solo cambio de email
		user = User.objects.get(username=infoUser['name'])
		user.email = infoUser['email']
		user.save()
		datos = "true"
		return HttpResponse(datos)
	if 'email' not in infoUser:
		if infoUser['password'] == infoUser['confirmPassword']:
			#solo cambio de pass
			user = User.objects.get(username=infoUser['name'])
			user.set_password(infoUser['password'])
			user.save()
			datos = "true"
			return HttpResponse(datos)
		#pass incorrectas
		datos = "WRONGPASS"
		return HttpResponse(datos)
	
	try:
		#cambiarlo todo(mail/pass)
		#User.objects.create_user(username=infoUser['username'], password=infoUser['password'], email=infoUser['email']).save()
		user = User.objects.get(username=infoUser['name'])
		user.email = infoUser['email']
		user.set_password(infoUser['password'])
		user.save()
		datos = "true"
	except:
		datos = "false"

	return HttpResponse(datos)

@csrf_exempt
def eventosDeUsuario(request):
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser or 'name' not in infoUser:
		return HttpResponse('false')

	try:
		user = User.objects.get(username=infoUser['name'])
		info = UsuarioRecompensa.objects.filter(user_id=user.id)
		prepareToSend = []

		for recompensa in info:
			prepareToSend.append(recompensa.returnJSON())

		datos = json.dumps(prepareToSend)
		return HttpResponse(datos)
	except:
		return HttpResponse('false')

@csrf_exempt
def provincias(request):
	infoUser = json.loads(str(request.body,"UTF-8"))
	if not infoUser or 'name' not in infoUser:
		return HttpResponse('false')
	try:
		provincias = Evento.objects.values_list('event_provincia').distinct()
		prepareToSend = []
		for provincia in provincias:
			prepareToSend.append(provincia)
		datos = json.dumps(prepareToSend)
		print(datos)
		return HttpResponse(datos)
	except:
		return HttpResponse('false')
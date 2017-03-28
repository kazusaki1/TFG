import PIL
from PIL import Image
import os

basewidth = 80
baseheight = 80
ruta = '../../../../../Images/'


if not os.path.exists('clases'):
	os.mkdir('clases')

for ficheroActual in os.listdir(ruta):
	if os.path.isdir(ruta+'/'+ficheroActual):	
		if not os.path.exists('clases/'+ficheroActual):
			os.mkdir('clases/'+ficheroActual)
		for imagen in os.listdir(ruta+'/'+ficheroActual):
			if len(imagen) > 15:
				cont = 0			
				nuevaImagen = str(cont)+imagen[-10:]
				nuevoFichero = ruta+ficheroActual+'/'+nuevaImagen
				while os.path.exists(nuevoFichero):
					cont += 1
					nuevaImagen = str(cont)+imagen[-10:]
					nuevoFichero = ruta+ficheroActual+'/'+nuevaImagen
				os.rename(ruta+ficheroActual+'/'+imagen,nuevoFichero)
				imagen = nuevaImagen
				
			img = Image.open(ruta+ficheroActual+'/'+imagen)
			wpercent = (basewidth / float(img.size[0]))
			hpercent = (baseheight / float(img.size[1]))
			img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
			if len(img.getbands()) != 1 and len(img.getbands()) != 4:
				img.save('clases/'+ficheroActual+'/'+imagen)
			if len(img.getbands()) == 4:
				background = Image.new("RGB", img.size, (255, 255, 255))
				background.paste(img, mask=img.split()[0])
				background.paste(img, mask=img.split()[1])
				background.paste(img, mask=img.split()[2])
				background.save('clases/'+ficheroActual+'/'+imagen)
			if img.getbands()[0] == "L":
				newImage = Image.merge("RGB", [img.split()[0],img.split()[0],img.split()[0]])
				newImage.save('clases/'+ficheroActual+'/'+imagen)
			if img.getbands()[0] == "P":	
				img = img.convert("RGBA")
				background = Image.new("RGB", img.size, (255, 255, 255))
				background.paste(img, mask=img.split()[0])
				background.paste(img, mask=img.split()[1])
				background.paste(img, mask=img.split()[2])
				background.save('clases/'+ficheroActual+'/'+imagen)
			

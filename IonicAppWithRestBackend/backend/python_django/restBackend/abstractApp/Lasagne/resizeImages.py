import PIL
from PIL import Image
import os
import numpy
from scipy import misc

basewidth = 80
baseheight = 80
ruta = '../../../../../../Images/'

if not os.path.exists('clases'):
	os.mkdir('clases')

for ficheroActual in os.listdir(ruta):
	print("Creating label -> " + ficheroActual)
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
				os.rename(os.path.abspath(ruta+ficheroActual+'/'+imagen),nuevoFichero)
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



			# Normalize image
			image = misc.imread('clases/'+ficheroActual+'/'+imagen)
			r = image[:,:,0]
			g = image[:,:,1]
			b = image[:,:,2]
			if r.max() != r.min() and r.max()-r.min() > 50:
				image[:,:,0] = (r-r.min())*(255.0/(r.max()-r.min()))
				image[:,:,1] = (g-g.min())*(255.0/(g.max()-g.min()))
				image[:,:,2] = (b-b.min())*(255.0/(b.max()-b.min()))
			misc.imsave('clases/'+ficheroActual+'/'+imagen, image)

			#if r.min() == 255:
			#	os.remove(os.path.abspath(ruta+ficheroActual+'/'+imagen))

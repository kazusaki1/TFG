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
			img = Image.open(ruta+'/'+ficheroActual+'/'+imagen)
			wpercent = (basewidth / float(img.size[0]))
			hpercent = (baseheight / float(img.size[1]))
			img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
			img.save('clases/'+ficheroActual+'/'+imagen)

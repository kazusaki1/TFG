
from __future__ import print_function

import sys
import os
import time

import numpy as np
import theano
import theano.tensor as T

import PIL
from PIL import Image

import lasagne
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from scipy import misc
import itertools

import matplotlib.pyplot as plt

def main(image_name, test_net, brand):

	classes_path = os.getcwd()+'\\abstractApp\\Lasagne\\' #change the path to your dataset folder here
	img_path = os.getcwd()+"\\uploaded_media\\"+image_name
	tmp_path = os.getcwd()+"\\uploaded_media\\tmp"+image_name
	classes = [folder for folder in os.listdir(classes_path+"clases")]

	print("Imagen:"+image_name)

	for x in range(0,7):

		image = transformImage(image_name,img_path,tmp_path,x)


		#we need to get the index of our label from classes
		index = classes.index("random")

		#allocate array for target
		target = np.zeros((10), dtype='float32')

		#we set our target array = 1.0 at our label index, all other entries remain zero
		#Example: if label = dog and dog has index 2 in classes, target looks like: [0.0, 0.0, 1.0, 0.0, 0.0]
		target[index] = 1.0

		#we need a 4D-vector for our image and a 2D-vector for our targets
		#we can adjust array dimension with reshape
		image = image.reshape(-1, 3, 80, 80)
		target = target.reshape(-1, 10)
		#mostrarConfusionMatrix()
		prediction, l, a = test_net(image, target)
		
		maxValue = 0
		maxInd = 0
		cont = 0
		for value in prediction[0]:
			if maxValue < value:
				maxValue = value
				maxInd = cont	
			cont = cont + 1

		print("Resultado " + str(x) + ": " + classes[maxInd] + " con " + str(maxValue) + ", Esperado: " + brand)

		
		if maxValue > 0.7 and brand == classes[maxInd]:
			return "true"

	return "false"

def transformImage(image_name,img_path,tmp_path,crop):

	img = Image.open(img_path)
	w, h = img.size
	if crop == 1:
		img = img.crop((0, 0, w/2, h))
	elif crop == 2:
		img = img.crop((0, 0, w, h/2))
	elif crop == 3:
		img = img.crop((0, 0, w/2, h/2))
	elif crop == 4:
		img = img.crop((w/2, 0, w, h/2))
	elif crop == 5:
		img = img.crop((0, h/2, w/2, h))
	elif crop == 6:
		img = img.crop((w/2, h/2, w, h))

	wpercent = (80 / float(img.size[0]))
	hpercent = (80 / float(img.size[1]))
	img = img.resize((80, 80), PIL.Image.ANTIALIAS)
	img.save(tmp_path)


	#here we open the image
	image = misc.imread(tmp_path)
	image = np.transpose(image, (2, 0, 1))
	os.remove(tmp_path)

	return image

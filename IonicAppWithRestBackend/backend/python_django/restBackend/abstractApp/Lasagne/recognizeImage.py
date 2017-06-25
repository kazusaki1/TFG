
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

	classes_path = os.getcwd()+'\\abstractApp\\Lasagne\\'
	img_path = os.getcwd()+"\\uploaded_media\\"+image_name
	tmp_path = os.getcwd()+"\\uploaded_media\\tmp"+image_name
	classes = [folder for folder in os.listdir(classes_path+"clases")]

	print("Imagen:"+image_name)

	index = classes.index("random")

	target = np.zeros((11), dtype='float32')

	target[index] = 1.0

	target = target.reshape(-1, 11)

	img = Image.open(img_path)

	for i in range(1,5):
		image = misc.imread(img_path)
		
		w = len(image[0])
		h = len(image)

		if w > h:
			diff = float(h)/80.0		
			
		else:
			diff = float(w)/80.0

		image = misc.imresize(image,[int(h/diff)*i,int(w/diff)*i])
		print(misc.info(image))

		# Normalize image
		r = image[:,:,0]
		g = image[:,:,1]
		b = image[:,:,2]
		if r.max() != r.min() and r.max()-r.min() > 50:
			image[:,:,0] = (r-r.min())*(255.0/(r.max()-r.min()))
			image[:,:,1] = (g-g.min())*(255.0/(g.max()-g.min()))
			image[:,:,2] = (b-b.min())*(255.0/(b.max()-b.min()))


		w = len(image[0])
		h = len(image)
		desp = 40
		size = 80
		currentW = 0
		currentH = 0

		while currentH <= h:
			if h - currentH < size:
				currentH = h - size
			if w - currentW < size:
				currentW = w - size

			tmp = image[currentH:currentH+size,currentW:currentW+size]

			tmp = tmp.reshape(-1, 3, 80, 80)

			prediction, l, a = test_net(tmp, target)
			
			maxValue = 0
			maxInd = 0
			cont = 0
			for value in prediction[0]:
				if maxValue < value:
					maxValue = value
					maxInd = cont	
				cont = cont + 1

			print("Resultado: " + classes[maxInd] + " con " + str(maxValue) + ", Esperado: " + brand)

			
			if maxValue > 0.7 and brand == classes[maxInd]:
				return "true"

			currentW = currentW + desp
			if currentW + desp >= w:
				currentW = 0
				if currentH + size >= h:
					currentH = h + 1
				else:
					currentH = currentH + desp

	return "false"
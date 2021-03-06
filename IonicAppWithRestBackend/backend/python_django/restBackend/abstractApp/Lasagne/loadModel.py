from __future__ import print_function

import sys
import os
import time

import numpy as np
import theano
import theano.tensor as T


import lasagne
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix

import itertools

import matplotlib.pyplot as plt

def loadModel():

	################### DATASET HANDLING ####################
	DATASET_PATH = os.getcwd()+'\\abstractApp\\Lasagne\\' #change the path to your dataset folder here
	def parseDataset():
	 
		#we use subfolders as class labels
		classes = [folder for folder in os.listdir(DATASET_PATH+"clases")]
	 
		#now we enlist all image paths
		images = []
		for c in classes:
			images += ([os.path.join(DATASET_PATH+"clases", c, path) for path in os.listdir(os.path.join(DATASET_PATH+"clases", c))])
	 
		#shuffle image paths
		images = shuffle(images, random_state=42)
	 
		#we want to use a 15% validation split
		vsplit = int(len(images) * 0.15)
		train = images[:-vsplit]
		val = images[-vsplit:]
	 
		#show some stats
		print("CLASS LABELS:", classes)
		print("TRAINING IMAGES:", len(train))
		print("VALIDATION IMAGES:", len(val))
	 
		return classes, train, val
	 
	#parse dataset
	CLASSES, TRAIN, VAL = parseDataset()


	def buildModel():
	 
	    #this is our input layer with the inputs (None, dimensions, width, height)
	    l_input = lasagne.layers.InputLayer((None, 3, 80, 80))
	 
	    #first convolutional layer, has l_input layer as incoming and is followed by a pooling layer
	    l_conv1 = lasagne.layers.Conv2DLayer(l_input, num_filters=32, filter_size=3, nonlinearity=lasagne.nonlinearities.rectify)
	    l_pool1 = lasagne.layers.MaxPool2DLayer(l_conv1, pool_size=2)
	 
	    #second convolution (l_pool1 is incoming), let's increase the number of filters
	    l_conv2 = lasagne.layers.Conv2DLayer(l_pool1, num_filters=64, filter_size=3, nonlinearity=lasagne.nonlinearities.rectify)
	    l_pool2 = lasagne.layers.MaxPool2DLayer(l_conv2, pool_size=2)
	 
	    #third and final convolution, even more filters
	    l_conv3 = lasagne.layers.Conv2DLayer(l_pool2, num_filters=64, filter_size=3, nonlinearity=lasagne.nonlinearities.rectify)
	    l_pool3 = lasagne.layers.MaxPool2DLayer(l_conv3, pool_size=2)
	 
	    l_dense1 = lasagne.layers.DenseLayer(l_pool3, num_units=1024, nonlinearity=lasagne.nonlinearities.rectify)

	    l_drop1 = lasagne.layers.dropout(l_dense1, p=.5)

	    l_dense2 = lasagne.layers.DenseLayer(l_drop1, num_units=1024)

	    #the output layer has 11 units which is exactly the count of our class labels
	    #it has a softmax activation function, its values represent class probabilities
	    l_output = lasagne.layers.DenseLayer(l_dense2, num_units=11, nonlinearity=lasagne.nonlinearities.softmax)
	 
	    #let's see how many params our net has
	    print("MODEL HAS", lasagne.layers.count_params(l_output), "PARAMS")
	 
	    #we return the layer stack as our network by returning the last layer
	    return l_output
	    
	    
	 
	NET = buildModel()

	# Optionally, you could now dump the network weights to a file like this:
	# np.savez('model.npz', *lasagne.layers.get_all_param_values(network))
	#
	# And load them again later on like this:
	with np.load(DATASET_PATH+'model.npz') as f:
		param_values = [f['arr_%d' % i] for i in range(len(f.files))]
	lasagne.layers.set_all_param_values(NET, param_values)

	#################### LOSS FUNCTION ######################
	def calc_loss(prediction, targets):
	 
		#categorical crossentropy is the best choice for a multi-class softmax output
		l = T.mean(lasagne.objectives.categorical_crossentropy(prediction, targets))
		
		return l
	 
	#theano variable for the class targets
	#this is the output vector the net should predict
	targets = T.matrix('targets', dtype=theano.config.floatX)
	 
	#get the network output
	prediction = lasagne.layers.get_output(NET)
	 
	#calculate the loss
	loss = calc_loss(prediction, targets)



	################# ACCURACY FUNCTION #####################
	def calc_accuracy(prediction, targets):
	 
		#we can use the lasagne objective categorical_accuracy to determine the top1 accuracy
		a = T.mean(lasagne.objectives.categorical_accuracy(prediction, targets, top_k=1))
		
		return a
	 
	accuracy = calc_accuracy(prediction, targets)

	####################### UPDATES #########################
	#get all trainable parameters (weights) of our net
	params = lasagne.layers.get_all_params(NET, trainable=True)
	 
	#we use the adam update
	#it changes params based on our loss function with the learning rate
	param_updates = lasagne.updates.adam(loss, params, learning_rate=0.00001)


	#################### TRAIN FUNCTION ######################
	#the theano train functions takes images and class targets as input
	#it updates the parameters of the net and returns the current loss as float value
	#compiling theano functions may take a while, you might want to get a coffee now...
	print("COMPILING THEANO TRAIN FUNCTION...")
	train_net = theano.function([lasagne.layers.get_all_layers(NET)[0].input_var, targets], loss, updates=param_updates)
	print("DONE!")
	 
	################# PREDICTION FUNCTION ####################
	#we need the prediction function to calculate the validation accuracy
	#this way we can test the net after training
	#first we need to get the net output
	net_output = lasagne.layers.get_output(NET)
	 
	#now we compile another theano function; this may take a while, too
	print("COMPILING THEANO TEST FUNCTION...")
	test_net = theano.function([lasagne.layers.get_all_layers(NET)[0].input_var, targets], [net_output, loss, accuracy])
	print("DONE!")



			
			
	 ##################### STAT PLOT #########################
	plt.ion()
	label_added = False
	def showChart(epoch, t, v, a):
	 
		#x-Axis = epoch
		e = range(0, epoch + 1)
	 
		#loss subplot
		plt.subplot(211)
		plt.plot(e, train_loss, 'r-', label='Train Loss')
		plt.plot(e, val_loss, 'b-', label='Val Loss')
		plt.ylabel('loss')
	 
		#show labels only once
		global label_added
		if not label_added:
			plt.legend(loc='upper right', shadow=True)
		label_added = True
	 
		#accuracy subplot
		plt.subplot(212)
		plt.plot(e, val_accuracy, 'g-')
		plt.ylabel('accuracy')
		plt.xlabel('epoch')
	 
		#show
		plt.show()
		plt.pause(0.5)
			
	   
	 
	################## CONFUSION MATRIX #####################
	cmatrix = []
	def clearConfusionMatrix():
	 
		global cmatrix
	 
		#allocate empty matrix of size 11x11 (for our 11 classes)
		cmatrix = np.zeros((11, 11), dtype='int32')
	 
	def updateConfusionMatrix(p, t):
	 
		global cmatrix
		cmatrix += confusion_matrix(np.argmax(t, axis=1), np.argmax(p, axis=1))
	 
	def showConfusionMatrix():
	 	
		global cmatrix
		#new figure
		plt.figure(1)
		plt.clf()
	 
		print(cmatrix)
		#show matrix
		plt.imshow(cmatrix, interpolation='nearest', cmap=plt.cm.Blues)
		plt.title('Confusion Matrix')
		plt.colorbar()
	 
		#tick marks
		tick_marks = np.arange(len(CLASSES))
		plt.xticks(tick_marks, CLASSES)
		plt.yticks(tick_marks, CLASSES)
	 
		#labels
		thresh = cmatrix.max() / 2.
		for i, j in itertools.product(range(cmatrix.shape[0]), range(cmatrix.shape[1])):
			plt.text(j, i, cmatrix[i, j], 
					 horizontalalignment="center",
					 color="white" if cmatrix[i, j] > thresh else "black")
	 
		#axes labels
		plt.ylabel('Target label')
		plt.xlabel('Predicted label')
	 
		#show
		plt.show()
		plt.pause(0.5)
	   
	   




	def mostrarConfusionMatrix():
		clearConfusionMatrix()
		for image_batch, target_batch in getNextImageBatch(VAL):
				
				#calling the test function returns the net output, loss and accuracy
				prediction_batch, l, a = test_net(image_batch, target_batch)
				updateConfusionMatrix(prediction_batch,target_batch)
		showConfusionMatrix()

	return test_net

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

################### DATASET HANDLING ####################
DATASET_PATH = os.getcwd()+'\\' #change the path to your dataset folder here
def parseDataset():
 
    #we use subfolders as class labels
    classes = [folder for folder in os.listdir(DATASET_PATH+"clases")]
 
    ficheroTrain = open ('datasetTrain.txt')
    ficheroTest = open ('datasetTest.txt')

    image = '1'
    train = []       
    while image != '':
        image = ficheroTrain.readline()
        if image != '':
            train.append(image)

    image = '1'
    test = []
    while image != '':
        image = ficheroTest.readline()
        if image != '':
            test.append(image)


    ficheroTrain.close()
    ficheroTest.close()


    #show some stats
    print("CLASS LABELS:", classes)
    print("TRAINING IMAGES:", len(train))
    print("TESTING IMAGES:", len(test))
 
    return classes, train, test
 
#parse dataset
CLASSES, TRAIN, TEST = parseDataset()

 
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

with np.load('model.npz') as f:
	param_values = [f['arr_%d' % i] for i in range(len(f.files))]
lasagne.layers.set_all_param_values(NET, param_values)



#with np.load(DATASET_PATH+'model.npz') as f:
#    param_values = [f['arr_%d' % i] for i in range(len(f.files))]
#lasagne.layers.set_all_param_values(NET, param_values)

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
#we need the prediction function to calculate the testing accuracy
#this way we can test the net after training
#first we need to get the net output
net_output = lasagne.layers.get_output(NET)
 
#now we compile another theano function; this may take a while, too
print("COMPILING THEANO TEST FUNCTION...")
test_net = theano.function([lasagne.layers.get_all_layers(NET)[0].input_var, targets], [net_output, loss, accuracy])
print("DONE!")

#################### BATCH HANDLING #####################
def loadImageAndTarget(path):

    #here we open the image
    img = misc.imread(path.replace('\\\\','\\')[:-1])
    
    #OpenCV uses BGR instead of RGB, but for now we can ignore that
    #our image has the shape (80, 80, 3) but we need it to be (3, 80, 80)
    img = np.transpose(img, (2, 0, 1))
    
    #we want to use subfolders as class labels
    label = path.split("\\")[-2]

    #we need to get the index of our label from CLASSES
    index = CLASSES.index(label)

    #allocate array for target
    target = np.zeros((11), dtype='float32')

    #we set our target array = 1.0 at our label index, all other entries remain zero
    #Example: if label = dog and dog has index 2 in CLASSES, target looks like: [0.0, 0.0, 1.0, 0.0, 0.0]
    target[index] = 1.0

    #we need a 4D-vector for our image and a 2D-vector for our targets
    #we can adjust array dimension with reshape
    img = img.reshape(-1, 3, 80, 80)
    target = target.reshape(-1, 11)

    return img, target

#a reasonable size for one batch is 100
BATCH_SIZE = 100

def getDatasetChunk(split):

    #get batch-sized chunks of image paths
    for i in range(0, len(split), BATCH_SIZE):
        yield split[i:i+BATCH_SIZE]

def getNextImageBatch(split=TRAIN):    

    #allocate numpy arrays for image data and targets
    #input shape of our ConvNet is (None, 3, 80, 80)
    x_b = np.zeros((BATCH_SIZE, 3, 80, 80), dtype='float32')
    #output shape of our ConvNet is (None, 11) as we have 11 classes
    y_b = np.zeros((BATCH_SIZE, 11), dtype='float32')

    #fill batch
    for chunk in getDatasetChunk(split):       
        ib = 0
        for path in chunk:
            #load image data and class label from path
            x, y = loadImageAndTarget(path)

            #pack into batch array
            x_b[ib] = x
            y_b[ib] = y
            ib += 1

        #instead of return, we use yield
        yield x_b[:len(chunk)], y_b[:len(chunk)]

        
        
 ##################### STAT PLOT #########################
plt.ion()
label_added = False
def showChart(epoch, t, v, a):
 
    #x-Axis = epoch
    e = range(0, epoch + 1)
 
    #loss subplot
    plt.subplot(211)
    plt.plot(e, train_loss, 'r-', label='Train Loss')
    plt.plot(e, test_loss, 'b-', label='Test Loss')
    plt.ylabel('loss')
 
    #show labels only once
    global label_added
    if not label_added:
        plt.legend(loc='upper right', shadow=True)
    label_added = True
 
    #accuracy subplot
    plt.subplot(212)
    plt.plot(e, test_accuracy, 'g-')
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
 
    #new figure
    plt.figure(1)
    plt.clf()
 
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
    


brand = "damm"
classes = [folder for folder in os.listdir("clases")]

print("Imagen: "+"prueba.jpeg")


#we need to get the index of our label from classes
index = classes.index(brand)

#allocate array for target
target = np.zeros((11), dtype='float32')

#we set our target array = 1.0 at our label index, all other entries remain zero
#Example: if label = dog and dog has index 2 in classes, target looks like: [0.0, 0.0, 1.0, 0.0, 0.0]
target[index] = 1.0

#we need a 2D-vector for our targets
#we can adjust array dimension with reshape
target = target.reshape(-1, 11)
#mostrarConfusionMatrix()



#img.show()

for i in range(1,5):
	image = misc.imread("prueba.jpeg")

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


	#print(len(image[0]))

	w = len(image[0])
	h = len(image)
	desp = 40
	size = 80
	currentW = 0
	currentH = 0
	#print(h)
	while currentH <= h:
		if h - currentH < size:
			currentH = h - size
		if w - currentW < size:
			currentW = w - size
		tmp = image[currentH:currentH+size,currentW:currentW+size]
	    #print(misc.info(tmp))
		

	    #we need a 4D-vector for our image
		#we can adjust array dimension with reshape
		tmp2 = tmp.reshape(-1, 3, 80, 80)


		prediction, l, a = test_net(tmp2, target)
		
		maxValue = 0
		maxInd = 0
		cont = 0
		#print(prediction)
		for value in prediction[0]:
			if maxValue < value:
				maxValue = value
				maxInd = cont	
			cont = cont + 1

		print("Resultado: " + classes[maxInd] + " con " + str(maxValue) + ", Esperado: " + brand)
		#if classes[maxInd] == brand:
		plt.imshow(tmp)
		plt.show(block=True)

		currentW = currentW + desp
		if currentW + desp >= w:
			currentW = 0
			if currentH + size >= h:
				currentH = h + 1
			else:
				currentH = currentH + desp





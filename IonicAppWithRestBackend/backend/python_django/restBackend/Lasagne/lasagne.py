import theano
import theano.tensor as T
import lasagne
import numpy as np
import os
from sklearn.utils import shuffle
from scipy import misc
import time




DATASET_PATH = 'clases'


def parseDataset():
	# ruta de las clases
	classes = [folder for folder in os.listdir(DATASET_PATH)]

	# guardamos la ruta de cada imagen
	images = []
	for c in classes:
		images += ([os.path.join(DATASET_PATH, c, path) for path in os.listdir(os.path.join(DATASET_PATH, c))])

	# mezclamos las imagenes
	images = shuffle(images, random_state=42)

	# usamos un 10% de las imagenes para el validation set
	vsplit = int(len(images) * 0.10)
	train = images[:-vsplit]
	val = images[-vsplit:]

	print("CLASS LABELS:", classes)
	print("TRAINING IMAGES:", len(train))
	print("VALIDATION IMAGES:", len(val))
	
	return classes, train, val


def buildModel():
 
    # input layer (None, dimensions, width, height)
    l_input = lasagne.layers.InputLayer((None, 3, 80, 80))
 
    # primer convolutional layer, le pasamos el input layer
    l_conv1 = lasagne.layers.Conv2DLayer(l_input, num_filters=32, filter_size=3)
	# pool layer 2x2
    l_pool1 = lasagne.layers.MaxPool2DLayer(l_conv1, pool_size=2)
	
    # segunda convolucion, le pasamos el resultado del maxpool
    l_conv2 = lasagne.layers.Conv2DLayer(l_pool1, num_filters=64, filter_size=3)
	# pool layer 2x2
    l_pool2 = lasagne.layers.MaxPool2DLayer(l_conv2, pool_size=2)
 
    # tercera convolucion
    l_conv3 = lasagne.layers.Conv2DLayer(l_pool2, num_filters=64, filter_size=3)
	# pool layer 2x2
    l_pool3 = lasagne.layers.MaxPool2DLayer(l_conv3, pool_size=2)
 
    # layer de 1024 posiciones
    l_dense1 = lasagne.layers.DenseLayer(l_pool3, num_units=1024)
	
	# dropout del 50%
    l_dropout = lasagne.layers.DenseLayer(lasagne.layers.dropout(l_dense1, p=.5),num_units=1024,nonlinearity=lasagne.nonlinearities.rectify)
	
    # la salida tiene tantas unidades como clases usemos y aplicamos un softmax
    l_output = lasagne.layers.DenseLayer(l_dropout, num_units=4, nonlinearity=lasagne.nonlinearities.softmax)
 
    print ("MODEL HAS", lasagne.layers.count_params(l_output), "PARAMS")
 
    # devolvemos el layer obtenido de la red
    return l_output


################# LOSS FUNCTION #####################
def calc_loss(prediction, targets):
 
    # calculamos las perdidas con un categorical crossentropy
    l = T.mean(lasagne.objectives.categorical_crossentropy(prediction, targets))
    
    return l




################# ACCURACY FUNCTION #####################
def calc_accuracy(prediction, targets):
 
    # calculamos el acierto con un categorical accuracy
    a = T.mean(lasagne.objectives.categorical_accuracy(prediction, targets, top_k=1))
    
    return a


 
 
#################### BATCH HANDLING #####################
def loadImageAndTarget(path):

	# leemos la imagen
	img = misc.imread(path)
	
    # como la imagen tiene formato 80x80x3 lo modificamos a 3x80x80
	img = np.transpose(img, (2,0,1))
	
	# usamos las carpetas de las clases como labels
	label = path.split("\\")[-2]
	
	# guardamos el index del label
	index = CLASSES.index(label)
	
	# inicializamos a 0 el array de labels de salida
	target = np.zeros((4), dtype='float32')
	
	# insertamos un 1.0 al label correspondiente, quedando un array asi: [0.0, 0.0, 1.0, 0.0] siendo 1.0 la clase de la imagen actual
	target[index] = 1.0
	
	# como necesitamos que la imagen sea un vector 4D y el array de labels un vector 2D los convertimos
	img = img.reshape(-1, 3, 80, 80)
	target = target.reshape(-1, 4)
	
	return img, target


def getDatasetChunk(split):
 
    # obtenemos las imagenes correspondientes al batch
    for i in range(0, len(split), BATCH_SIZE):
        yield split[i:i+BATCH_SIZE]
		
def getNextImageBatch(split):    
 
    # inicializamos a 0 el array de la imagen 
    x_b = np.zeros((BATCH_SIZE, 3, 80, 80), dtype='float32')
    # inicializamos a 0 el array de los labels
    y_b = np.zeros((BATCH_SIZE, 4), dtype='float32')
 
	#rellenamos el batch
    for chunk in getDatasetChunk(split):        
        ib = 0
        for path in chunk:
            # cargamos la imagen y label
            x, y = loadImageAndTarget(path)
 
            # lo guardamos dentro del array de batch
            x_b[ib] = x
            y_b[ib] = y
            ib += 1
 
        yield x_b[:len(chunk)], y_b[:len(chunk)]
		

CLASSES, TRAIN, VAL = parseDataset()		

network = buildModel()
	
#theano variable for the class targets
#this is the output vector the net should predict
targets = T.matrix('targets', dtype=theano.config.floatX)
 
#get the network output
prediction = lasagne.layers.get_output(network)
 
#calculate the loss
loss = calc_loss(prediction, targets)

#calculate the accuracy
accuracy = calc_accuracy(prediction, targets)
 
####################### UPDATES #########################
#get all trainable parameters (weights) of our net
params = lasagne.layers.get_all_params(network, trainable=True)
 
#we use the adam update
#it changes params based on our loss function with the learning rate
param_updates = lasagne.updates.adam(loss, params, learning_rate=0.00001)



#################### TRAIN FUNCTION ######################
#the theano train functions takes images and class targets as input
#it updates the parameters of the net and returns the current loss as float value
#compiling theano functions may take a while, you might want to get a coffee now...
print ("COMPILING THEANO TRAIN FUNCTION...")
train_net = theano.function([lasagne.layers.get_all_layers(network)[0].input_var, targets], loss, updates=param_updates)
print ("DONE!")
 
################# PREDICTION FUNCTION ####################
#we need the prediction function to calculate the validation accuracy
#this way we can test the net after training
#first we need to get the net output
net_output = lasagne.layers.get_output(network)
 
#now we compile another theano function; this may take a while, too
print ("COMPILING THEANO TEST FUNCTION...")
test_net = theano.function([lasagne.layers.get_all_layers(network)[0].input_var, targets], [net_output, loss, accuracy])
print ("DONE!")
	
#a reasonable size for one batch is 128
BATCH_SIZE = 128
 
###################### TRAINING #########################
print ("START TRAINING...")
train_loss = []
val_loss = []
val_accuracy = []
for epoch in range(0, 100):
 
    #start timer
    start_time = time.time()
 
    #iterate over train split batches and calculate mean loss for epoch
    t_l = []
    for image_batch, target_batch in getNextImageBatch(TRAIN):
 
        #calling the training functions returns the current loss
        l = train_net(image_batch, target_batch)
        t_l.append(l)
 
    #we validate our net every epoch and pass our validation split through as well
    v_l = []
    v_a = []
    for image_batch, target_batch in getNextImageBatch(VAL):
 
        #calling the test function returns the net output, loss and accuracy
        prediction_batch, l, a = test_net(image_batch, target_batch)
        v_l.append(l)
        v_a.append(a)
 
 
    #calculate stats for epoch
    train_loss.append(np.mean(t_l))
    val_loss.append(np.mean(v_l))
    val_accuracy.append(np.mean(v_a))
 
    #print stats for epoch
    print ("EPOCH:", epoch)
    print ("TRAIN LOSS:", train_loss[-1])
    print ("VAL LOSS:", val_loss[-1])
    print ("VAL ACCURACY:", (int(val_accuracy[-1] * 1000) / 10.0), "%")
    print ("TIME:", time.time() - start_time)

 
print ("TRAINING DONE!")

 
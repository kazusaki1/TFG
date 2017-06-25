
from __future__ import print_function


import os
from sklearn.utils import shuffle
import numpy as np


################### DATASET HANDLING ####################
DATASET_PATH = os.getcwd()+'\\' #change the path to your dataset folder here
ficheroTrain = open ('datasetTrain.txt', 'w')
ficheroTest = open ('datasetTest.txt', 'w')

 
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
test = images[-vsplit:]

for image in train:
    ficheroTrain.write(image + '\n')

for image in test:
    ficheroTest.write(image + '\n')

#show some stats
print("CLASS LABELS:", classes)
print("TRAINING IMAGES:", len(train))
print("VALIDATION IMAGES:", len(test))

ficheroTrain.close()
ficheroTest.close()







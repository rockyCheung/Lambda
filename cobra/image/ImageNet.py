# -*- coding:utf-8 -*-
from cobra.conf.GlobalSettings import *
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from cobra.conf.GlobalSettings import *
import numpy as np
from keras.datasets import cifar10
from keras.utils import plot_model
# (X_train, y_train), (X_test, y_test) = cifar10.load_data()
model = ResNet50(weights='imagenet')
plot_model(model, to_file=ROOT_PATH+'/imagenet/model.png')
# img_path = ROOT_PATH+'/images/deer.jpg'
# img_path = ROOT_PATH+'/images/horse.jpg'
# img_path = ROOT_PATH+'/images/canglaoshi.jpeg'
img_path = ROOT_PATH+'/images/pig.jpeg'
# img_path = ROOT_PATH+'/images/chuanpu2.jpeg'
# img_path = ROOT_PATH+'/images/Saluki.jpg'
#img_path = ROOT_PATH+'/images/elephant.jpg'
img = image.load_img(img_path, target_size=(224, 224))
# print img
x = image.img_to_array(img)
# print x
x = np.expand_dims(x, axis=0)
# print x
x = preprocess_input(x)
# print x
preds = model.predict(x)
# decode the results into a list of tuples (class, description, probability)
# (one such list for each sample in the batch)
print('Predicted:', decode_predictions(preds, top=3)[0])
# Predicted: [(u'n02504013', u'Indian_elephant', 0.82658225), (u'n01871265', u'tusker', 0.1122357), (u'n02504458', u'African_elephant', 0.061040461)]
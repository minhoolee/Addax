"""Different deep learning models whose architectures were tested"""

import keras.backend as K
from keras import layers, metrics, objectives
from keras.models import Sequential, Model
from keras.layers import Input
from keras.layers.core import Dense, Dropout, Activation, Flatten, Reshape
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.layers.convolutional import Conv2D, MaxPooling1D
from keras.layers.normalization import BatchNormalization
from keras.layers.recurrent import LSTM, GRU
from keras.layers.wrappers import Bidirectional
from keras.layers.pooling import GlobalAveragePooling1D, AveragePooling1D
from keras.utils.layer_utils import convert_all_kernels_in_model
from keras.utils.data_utils import get_file
from keras.optimizers import SGD, Adam
from keras.regularizers import l2

from src.logging import log_utils

def crnn(self, input_shape=(0, 0, 0)):
	"""Build a CNN into RNN.

	Starting version from:
	https://github.com/udacity/self-driving-car/blob/master/
		steering-models/community-models/chauffeur/models.py
	"""

	model = Sequential()

	model.add(TimeDistributed(Conv2D(32, (3,3),
		kernel_initializer="he_normal",
		activation='relu'), input_shape=input_shape)
	model.add(TimeDistributed(Conv2D(32, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(MaxPooling2D()))

	model.add(TimeDistributed(Conv2D(48, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(Conv2D(48, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(MaxPooling2D()))

	model.add(TimeDistributed(Conv2D(64, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(Conv2D(64, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(MaxPooling2D()))

	model.add(TimeDistributed(Conv2D(128, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(Conv2D(128, (3,3),
		kernel_initializer="he_normal",
		activation='relu')))
	model.add(TimeDistributed(MaxPooling2D()))

	model.add(TimeDistributed(Flatten()))
	model.add(LSTM(256, return_sequences=True))
	model.add(Flatten())
	model.add(Dense(512))
	model.add(Dropout(0.5))
	model.add(Dense(self.nb_classes, activation='softmax'))

	return model


# def _mult_conv_max(model=None, nb_conv=1, nb_filter=64):
#     for i in range(nb_conv):
#         model.add(Convolution1D(input_dim=4,
#                                 input_length=1000,
#                                 nb_filter=nb_filter,
#                                 filter_length=3,
#                                 border_mode='same',
#                                 # init='he_normal',
#                                 subsample_length=1))
#         model.add(Activation('relu'))
#     model.add(MaxPooling1D(pool_length=2, stride=2))
#
# def vgg_net():
#     """
#     https://arxiv.org/pdf/1409.1556.pdf
#     """
#     _log.info('Building the model')
#     model = Sequential()
#     _mult_conv_max(model, nb_conv=2, nb_filter=64)
#     _mult_conv_max(model, nb_conv=2, nb_filter=128)
#     _mult_conv_max(model, nb_conv=3, nb_filter=256)
#     _mult_conv_max(model, nb_conv=3, nb_filter=512)
#     _mult_conv_max(model, nb_conv=3, nb_filter=512)
#
#     model.add(Flatten())
#     model.add(Dense(output_dim=4000))
#     model.add(Activation('relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(output_dim=4000))
#     model.add(Activation('relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(output_dim=919))
#     model.add(Activation('sigmoid'))
#
#     # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
#     # model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
#     _log.info('Compiling model')
#     model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model
#
#
# def vgg_net_16(weights='imagenet'):
#     '''Instantiate the VGG16 architecture,
#     optionally loading weights pre-trained
#     on ImageNet. Note that when using TensorFlow,
#     for best performance you should set
#     `image_dim_ordering="tf"` in your Keras config
#     at ~/.keras/keras.json.
#     The model and the weights are compatible with both
#     TensorFlow and Theano. The dimension ordering
#     convention used by the model is the one
#     specified in your Keras config file.
#     # Arguments
#         weights: one of `None` (random initialization)
#             or "imagenet" (pre-training on ImageNet).
#     # Returns
#         A Keras model instance.
#     '''
#
#     TH_WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_th_dim_ordering_th_kernels.h5'
#     TF_WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels.h5'
#
#     if weights not in {'imagenet', None}:
#         raise ValueError('The `weights` argument should be either ' \
#                          '`None` (random initialization) or `imagenet` ' \
#                          '(pre-training on ImageNet).')
#
#     _log.info('Building the model')
#     # Block 1
#     model = Sequential()
#     model.add(Convolution1D(input_dim=4, input_length=1000, 
#                             nb_filter=64, filter_length=3, activation='relu', border_mode='same', name='block1_conv1'))
#     model.add(Convolution1D(nb_filter=64, filter_length=3, activation='relu', border_mode='same', name='block1_conv2'))
#     model.add(MaxPooling1D(pool_length=2, stride=2, name='block1_pool'))
#
#     # Block 2
#     model.add(Convolution1D(nb_filter=128, filter_length=3,activation='relu', border_mode='same', name='block2_conv1'))
#     model.add(Convolution1D(nb_filter=128, filter_length=3, activation='relu', border_mode='same', name='block2_conv2'))
#     model.add(MaxPooling1D(pool_length=2, stride=2, name='block2_pool'))
#
#     # Block 3
#     model.add(Convolution1D(nb_filter=256, filter_length=3, activation='relu', border_mode='same', name='block3_conv1'))
#     model.add(Convolution1D(nb_filter=256, filter_length=3, activation='relu', border_mode='same', name='block3_conv2'))
#     model.add(Convolution1D(nb_filter=256, filter_length=3, activation='relu', border_mode='same', name='block3_conv3'))
#     model.add(MaxPooling1D(pool_length=2, stride=2, name='block3_pool'))
#
#     # Block 4
#     model.add(Convolution1D(nb_filter=512, filter_length=3, activation='relu', border_mode='same', name='block4_conv1'))
#     model.add(Convolution1D(nb_filter=512, filter_length=3, activation='relu', border_mode='same', name='block4_conv2'))
#     model.add(Convolution1D(nb_filter=512, filter_length=3, activation='relu', border_mode='same', name='block4_conv3'))
#     model.add(MaxPooling1D(pool_length=2, stride=2, name='block4_pool'))
#
#     # Block 5
#     model.add(Convolution1D(nb_filter=512, filter_length=3, activation='relu', border_mode='same', name='block5_conv1'))
#     model.add(Convolution1D(nb_filter=512, filter_length=3, activation='relu', border_mode='same', name='block5_conv2'))
#     model.add(Convolution1D(nb_filter=512, filter_length=3, activation='relu', border_mode='same', name='block5_conv3'))
#     model.add(MaxPooling1D(pool_length=2, stride=2, name='block5_pool'))
#
#     # Classification block
#     model.add(Flatten(name='flatten'))
#     model.add(Dense(4096, activation='relu', name='fc1'))
#     model.add(Dense(4096, activation='relu', name='fc2'))
#     # model.add(Dense(1000, activation='softmax', name='predictions'))
#
#     # load weights
#     if weights == 'imagenet':
#         _log.info('K.image_dim_ordering:', K.image_dim_ordering())
#         if K.image_dim_ordering() == 'th':
#             weights_path = get_file('vgg_net_16.h5',
#                                     TH_WEIGHTS_PATH,
#                                     cache_subdir='models')
#             model.load_weights(weights_path)
#             if K.backend() == 'tensorflow':
#                 warnings.warn('You are using the TensorFlow backend, yet you '
#                               'are using the Theano '
#                               'image dimension ordering convention '
#                               '(`image_dim_ordering="th"`). '
#                               'For best performance, set '
#                               '`image_dim_ordering="tf"` in '
#                               'your Keras config '
#                               'at ~/.keras/keras.json.')
#                 convert_all_kernels_in_model(model)
#         else:
#             weights_path = get_file('vgg_net_16.h5',
#                                     TF_WEIGHTS_PATH,
#                                     cache_subdir='models')
#             model.load_weights(weights_path)
#             if K.backend() == 'theano':
#                 convert_all_kernels_in_model(model)
#
#     _log.info('Compiling model')
#     model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model

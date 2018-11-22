# -*- coding: utf-8 -*-
"""
LSTM实验版本

"""

import tensorflow as tf
from tensorflow.contrib import rnn

import numpy as np
import input_data

# 输入向量的维度
input_vec_size = lstm_size = 28
# 循环层长度
time_step_size = 28

batch_size = 128
test_size = 256

def init_weights(shape):
    # ???TODO
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, W, B, lstm_size):
    #
    XT = tf.transpose(X, [1, 0, 2])
    #
    XR = tf.reshape(XT, [-1, lstm_size])

    X_split = tf.split(XR, time_step_size, 0)

    lstm = rnn.BasicLSTMCell(lstm_size, forget_bias=1.0, state_is_tuple=True)
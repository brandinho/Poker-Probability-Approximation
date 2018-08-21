#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 21:41:58 2018

@author: brandinho
"""

import numpy as np
import tensorflow as tf

class probabilityApproximator():
    def __init__(self, sess, n_features, lr, use_existing_model, graph = None):
        self.sess = sess
        self._n_features = n_features
        self._neurons1 = 24
        self._neurons2 = 12
        
        if use_existing_model == True:
            self.inputs = graph.get_tensor_by_name("ProbabilityNetwork/Inputs:0")
            self.simulated_probability = graph.get_tensor_by_name("ProbabilityNetwork/ActualProbability:0")
            
            self.approximate_probability = graph.get_tensor_by_name("ProbabilityNetwork/Probability:0")
        else:
            with tf.variable_scope('ProbabilityNetwork'):        
                self.inputs = tf.placeholder(shape = [None, self._n_features], dtype = tf.float32, name = "Inputs")
                self.simulated_probability = tf.placeholder(shape = [None, 2], dtype = tf.float32, name = "ActualProbability")
                
                self.weights = tf.Variable(tf.random_normal([self._n_features, self._neurons1], stddev = tf.sqrt(2/(self._n_features + self._neurons1))))
                self.bias = tf.Variable(tf.zeros([1, self._neurons1]) + 0.01)
                self.layer = tf.nn.elu(tf.matmul(self.inputs, self.weights) + self.bias)
                
                self.weights2 = tf.Variable(tf.random_normal([self._neurons1, self._neurons2], stddev = tf.sqrt(2/(self._neurons1 + self._neurons2))))
                self.bias2 = tf.Variable(tf.zeros([1, self._neurons2]) + 0.01)
                self.layer2 = tf.nn.elu(tf.matmul(self.layer, self.weights2) + self.bias2)        
                
                self.weights3 = tf.Variable(tf.random_normal([self._neurons2, 2], stddev = tf.sqrt(2/(self._neurons2 + 2))))
                self.bias3 = tf.Variable(tf.zeros([1, 2]) + 0.01)
                self.approximate_probability = tf.nn.sigmoid(tf.matmul(self.layer2, self.weights3) + self.bias3, name = "Probability")               
        
        with tf.variable_scope("Loss"):
            self.loss = tf.reduce_mean(tf.square(self.simulated_probability - self.approximate_probability))
            
        with tf.variable_scope("TrainNetwork"):
            if use_existing_model == True:
                self.train_op = tf.get_collection("Trainer", scope = "TrainNetwork")[0]
            else:
                optimizer = tf.train.AdamOptimizer(lr)
                self.train_op = optimizer.minimize(self.loss)
                tf.add_to_collection(name = "Trainer", value = self.train_op)
        
    def trainModel(self, inputs, simulated_probability, epochs, batch_size, inputs_test, simulated_probability_test, verbose = True):
        
        batches_per_epoch = inputs.shape[0]//batch_size
        training_error_array = np.zeros(epochs)
        testing_error_array = np.zeros(epochs)
        
        for i in range(epochs):
            shuffled_indexes = np.random.choice(inputs.shape[0], size = inputs.shape[0], replace = False)
            batch_num = 0
            epoch_error = 0
            for j in range(batches_per_epoch):
                current_index = shuffled_indexes[batch_num:(batch_num + batch_size)]
                current_X = inputs[current_index,]
                current_Y = simulated_probability[current_index,]
                
                _, error = self.sess.run([self.train_op, self.loss], {self.inputs: current_X, self.simulated_probability: current_Y})
                
                epoch_error += error
                batch_num += batch_size
            epoch_error /= batches_per_epoch
            if i % 100 == 0 and verbose == True:
                print("The error for epoch {} is {}".format(i, epoch_error))
            training_error_array[i] = self.sess.run(self.loss, {self.inputs: inputs, self.simulated_probability: simulated_probability})
            testing_error_array[i] = self.sess.run(self.loss, {self.inputs: inputs_test, self.simulated_probability: simulated_probability_test})
            
        return training_error_array, testing_error_array
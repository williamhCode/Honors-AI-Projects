#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 21:46:35 2021

@author: williamhou
"""

import random
import time

class Neuron:
    
    def __init__(self, input_count, learning_rate=None, max_error=None, max_iterations=None):
        self.input_count = input_count
        self.learning_rate = learning_rate or 0.3
        self.max_error = max_error or 0
        self.max_iterations = max_iterations or 5000
        self.weights = self.generateWeights(self.input_count)  
        self.proceed = False
        
    def train(self, training_set_in, training_set_target):
        self.running = True
        iterations = 0
        while(iterations < self.max_iterations):
            while(not self.proceed):
                time.sleep(20/1000)
            self.proceed = False
            error_sum = 0
            i = 0
            while(i < len(training_set_in)):
                summation = -1 * self.weights[0]
                j = 0
                while(j < len(training_set_in[i])):
                    summation += training_set_in[i][j] * self.weights[j+1]
                    j += 1
                output = 1 if summation > 0 else 0
                error = training_set_target[i] - output
                error_sum += abs(error)
                self.weights[0] += self.learning_rate * error * -1
                j = 1
                while(j < len(self.weights)):
                    self.weights[j] += self.learning_rate * error * training_set_in[i][j-1]
                    j += 1
                i += 1
            iterations += 1
            print(error_sum)
            if(error_sum <= self.max_error):
                break
        self.running = False
        
    def nextIteration(self):
        self.proceed = True
        
    def activateNeuron(self, inputs):
        summation = -1 * self.weights[0]
        i = 0
        while(i < len(inputs)):
            summation += inputs[i] * self.weights[i+1]
            i += 1
        
        return 1 if summation > 0 else 0
    
    def generateWeights(self, size):
        outputList = [0] * (size+1)
        i = 0
        while(i < size):
            outputList[i] = random.random()*(4/10)-0.5
            i += 1
        
        return outputList
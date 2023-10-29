# -*- coding: utf-8 -*-


import random
import time

class _neuron:
    
    def __init__(self, input_count, learning_rate=None, max_error=None, max_iterations=None):
        self.input_count = input_count
        self.learning_rate = learning_rate or 0.3
        self.max_error = max_error or 0
        self.max_iterations = max_iterations or 5000
        self.weights = self.generateWeights(self.input_count) 
        
    def train(self, training_set_in, training_set_target):
        iterations = 0
        for iterations in range(self.max_iterations):
            error_sum = 0
            for i in range(len(training_set_in)):
                
                summation = -1 * self.weights[0]
                for j in range(len(training_set_in[i])):
                    summation += training_set_in[i][j] * self.weights[j+1]
                    
                output = 1 if summation > 0 else 0
                error = training_set_target[i] - output
                error_sum += abs(error)
                
                self.weights[0] += self.learning_rate * error * -1
                for j in range(len(self.weights)-1):
                    self.weights[j+1] += self.learning_rate * error * training_set_in[i][j]
                    
            if(error_sum <= self.max_error):
                break
        
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
        while(i < size+1):
            outputList[i] = random.random() + 1
            i += 1
        
        return outputList
            
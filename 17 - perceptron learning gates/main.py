#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 21:46:07 2021

@author: williamhou
"""

import threading
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation

from neuron import Neuron

ax = 0

neuron_1 = Neuron(3, 0.1, 0, 30)

training_set_in = [[0,0,0],
                   [1,0,0],
                   [0,1,0],
                   [0,0,1],
                  
                   [1,1,1],
                   [0,1,1],
                   [1,0,1],
                   [1,1,0]]

training_set_target = [0,0,0,0, 1,0,0,1]


def generateList(training_set_in):
    x = []
    y = []
    z = []
    
    i = 0
    while(i < len(training_set_in)):
        x.append(training_set_in[i][0])
        i += 1
    i = 0
    while(i < len(training_set_in)):
        y.append(training_set_in[i][1])
        i += 1
    i = 0
    while(i < len(training_set_in)):
        z.append(training_set_in[i][2])
        i += 1

    return x,y,z

def setAxes(ax):
    ax.set(xlabel='x', ylabel='y', zlabel='z')
    ax.set_xlim3d([-0.5, 1.5])
    ax.set_ylim3d([-0.5, 1.5])
    ax.set_zlim3d([-0.5, 1.5])
    ax.set_autoscale_on(False)

def background():
    neuron_1.train(training_set_in, training_set_target)
    
def main():
    global ax
    ax = plt.axes(projection='3d')
    setAxes(ax)
    
    x,y,z = generateList(training_set_in)
    
    ax.scatter(x,y,z)
    
    def animate(frame):
        a,b,c,d = neuron_1.weights[1], neuron_1.weights[2], neuron_1.weights[3], neuron_1.weights[0]
    
        x = np.linspace(-0.5,1.5,10)
        y = np.linspace(-0.5,1.5,10)
        
        X,Y = np.meshgrid(x,y)
        Z = (d - a*X - b*Y) / c
        
        ax.plot_surface(X, Y, Z, alpha=0.2)
        
        neuron_1.nextIteration()
        
        if(neuron_1.running == False):
            plt.cla()
            x,y,z = generateList(training_set_in)
            setAxes(ax)
            
            colors = []
            i = 0
            while(i < len(training_set_in)):
                if(neuron_1.activateNeuron(training_set_in[i]) == 0):
                    colors.append('red')
                else:
                    colors.append('green')
                i += 1
            ax.scatter(x,y,z,color=colors)
            ax.plot_surface(X, Y, Z, alpha=0.5)
            animation.event_source.stop()
            # inputs()
    
    animation = FuncAnimation(plt.gcf(), animate, interval=500)
    
    plt.show()

def inputs():
    while(True):
        boo = True
        while boo:
            try:
               x = input('Enter x:')
               x = int(x)
               boo = False
            except ValueError:
                print("Enter int!")
                boo = True
        while boo:
            try:
               y = input('Enter y:')
               y = int(y)
               boo = False
            except ValueError:
                print("Enter int!")
                boo = True
        while boo:
            try:
               z = input('Enter z:')
               z = int(z)
               boo = False
            except ValueError:
                print("Enter int!")
                boo = True

        colors = []
        if(neuron_1.activateNeuron([x,y,z]) == 0):
            colors.append('red')
        else:
            colors.append('green')
        ax.scatter([x,y,z], color=colors)
    
    
b = threading.Thread(target=background)
b.start()

main()
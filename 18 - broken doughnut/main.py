"""
Created on Tue Mar 16 10:29:52 2021

@author: williamhou
"""

import threading
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

import random
import math
import time

from neuron import _neuron
from point import point3D

def setAxes(ax):
    ax.set_xlim3d([-15, 15])
    ax.set_ylim3d([-15, 15])
    ax.set_zlim3d([-11, 11])
    ax.set_autoscale_on(False)
    
def generatePoint(radius, distance, width, label, neutral):
    # generate position on disk
    # https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly
    r = width/2 * math.sqrt(random.random())
    theta = 2 * math.pi * random.random()
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    
    if label == 'top':
        theta = math.pi * (random.random())
        
        disk_position = [x * math.cos(theta), y, x * math.sin(theta)]
        position_on_circumference = [radius * math.cos(theta), 0, radius * math.sin(theta)]
        central_displacement = [-radius/2, 0, distance/2]
        
        output_point = zip(disk_position, position_on_circumference, central_displacement)
        output_point = [sum(item) for item in output_point]
    
        if neutral:
            return point3D(output_point, -1)
        return point3D(output_point, 0)

    if label == 'bottom':
        theta = math.pi * (random.random()+1)
        
        disk_position = [x * math.cos(theta), y, x * math.sin(theta)]
        position_on_circumference = [radius * math.cos(theta), 0, radius * math.sin(theta)]
        central_displacement = [radius/2, 0, -distance/2]
        
        output_point = zip(disk_position, position_on_circumference, central_displacement)
        output_point = [sum(item) for item in output_point]
        
        if neutral:
            return point3D(output_point, -1)
        return point3D(output_point, 1)
    
def generateHalfMoon(amount, radius, distance, width, label, neutral):
    outputList = []
    i = 0
    while(i < amount):
        outputList.append(generatePoint(radius, distance, width, label, neutral))
        i += 1
        
    return outputList

def generateList(inputList):
    x = []
    y = []
    z = []
    colors = []
    
    i = 0
    while(i < len(inputList)):
        point = inputList[i]
        x.append(point.point[0])
        y.append(point.point[1])
        z.append(point.point[2])
        colors.append(point.getColor())
        i += 1
        
    return x,y,z,colors

def generatePlane(inputNeuron):
    a,b,c,d = inputNeuron.weights[1], inputNeuron.weights[2], inputNeuron.weights[3], inputNeuron.weights[0]
    
    x = np.linspace(-20,20,10)
    y = np.linspace(-10,10,10)
    
    X,Y = np.meshgrid(x,y)
    Z = (d - a*X - b*Y) / c
    
    return X,Y,Z
    
def label_to_color(label):
    if label == 0:
        return 'red'
    return 'blue'

def main():
    plt.figure(figsize=(10,9))
    ax = plt.axes(projection='3d')
    plt.axis('off')
    setAxes(ax)
    
    
    # Generate Half Moons
    radius = 10
    distance = 0
    width = 5
    amount = 1000
    
    training_set = []
    training_set += generateHalfMoon(amount, radius, distance, width, 'top', False)
    training_set += generateHalfMoon(amount, radius, distance, width, 'bottom', False)
    
    x,y,z,colors = generateList(training_set)
    ax.scatter(x, y, z, color=colors)
    
    # Split list of points into training set In and Out
    training_set_in = []
    training_set_target = []
    
    i = 0
    while(i < len(training_set)):
        point = training_set[i]
        training_set_in.append(point.point)
        training_set_target.append(point.label)
        i += 1
    
    neuron_1 = _neuron(3, 0.01, 0, 5)
    neuron_1.setMode(True)
      
    def background():
        neuron_1.train(training_set_in, training_set_target)
        
    bg = threading.Thread(target=background)
    bg.start()
    
    plt.pause(3)
    
    while True:
        plt.pause(0.5)
        
        X,Y,Z = generatePlane(neuron_1)
        ax.plot_surface(X, Y, Z, alpha=0.2)
        
        neuron_1.nextIteration()
        
        if(not bg.is_alive()):
            ax.cla()
            plt.axis('off')
            setAxes(ax)
            
            x,y,z,colors = generateList(training_set)
            ax.scatter(x, y, z, color=colors)
            
            ax.plot_surface(X, Y, Z, alpha=0.5)
            
            break
    
    plt.pause(3)
    
    plt.cla()
    plt.axis('off')
    setAxes(ax)
    
    training_set = []
    training_set += generateHalfMoon(amount, radius, distance, width, 'top', True)
    training_set += generateHalfMoon(amount, radius, distance, width, 'bottom', True)

    random.shuffle(training_set)
    
    X,Y,Z = generatePlane(neuron_1)
    ax.plot_surface(X, Y, Z, alpha=0.5)

    x,y,z,colors = generateList(training_set)
    
    global scat
    scat = ax.scatter(x, y, z, color=colors)
    
    start = time.time()
    
    def update(frame):
        global scat
        scat.remove()
        
        if(frame % 100 == 0):
            print('Frame: {}'.format(frame))
            print('Time: {}'.format(time.time() - start))
            print()
        
        colors[frame] = label_to_color(neuron_1.activateNeuron(training_set[frame].point))
        
        scat = ax.scatter(x, y, z, color=colors)
        
        if frame >= 1999:
            print('Frame: {}'.format(frame))
            print('Time: {}'.format(time.time() - start))
            ani.event_source.stop()
        
    ani = FuncAnimation(plt.gcf(), update, interval=1)
    
    plt.show()
    
scat = 0
        
if __name__ == "__main__":
    main()
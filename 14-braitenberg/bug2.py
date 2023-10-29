#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:33:54 2021

@author: williamhou
"""

import math

class bug_2:
    
    def __init__(self, xpos, ypos, rotation, distance, sensor_width, wheel_width, mode):
        self.xpos = xpos
        self.ypos = ypos
        self.rotation = rotation
        self.distance = distance
        self.sensor_width = sensor_width
        self.wheel_width = wheel_width
        self.mode = mode
        
    def sense(self, light_xpos, light_ypos):
        self.sensorL_xpos = self.xpos + self.distance * math.cos(math.radians(self.rotation + 90)) + self.sensor_width/2 * math.cos(math.radians(self.rotation + 180))
        self.sensorL_ypos = self.ypos - self.distance * math.sin(math.radians(self.rotation + 90)) - self.sensor_width/2 * math.sin(math.radians(self.rotation + 180))
        self.sensorR_xpos = self.xpos + self.distance * math.cos(math.radians(self.rotation + 90)) + self.sensor_width/2 * math.cos(math.radians(self.rotation))
        self.sensorR_ypos = self.ypos - self.distance * math.sin(math.radians(self.rotation + 90)) - self.sensor_width/2 * math.sin(math.radians(self.rotation))
        self.light_xpos = light_xpos     
        self.light_ypos = light_ypos
        
        self.wheelL_xpos = self.xpos + self.wheel_width/2 * math.cos(math.radians(self.rotation + 180))
        self.wheelL_ypos = self.ypos - self.wheel_width/2 * math.sin(math.radians(self.rotation + 180))
        self.wheelR_xpos = self.xpos + self.wheel_width/2 * math.cos(math.radians(self.rotation))
        self.wheelR_ypos = self.ypos - self.wheel_width/2 * math.sin(math.radians(self.rotation))
        
    def decide(self):
        constant = 100
        shift = -50
        power = 1.1
        
        sensorL_to_light_distance = ((self.sensorL_xpos - self.light_xpos)**2 + (self.sensorL_ypos - self.light_ypos)**2)**0.5
        sensorR_to_light_distance = ((self.sensorR_xpos - self.light_xpos)**2 + (self.sensorR_ypos - self.light_ypos)**2)**0.5
        
        self.intensityL = constant * 1/ (sensorL_to_light_distance - shift)**power
        self.intensityR = constant * 1/ (sensorR_to_light_distance - shift)**power
           
    def act(self, dt):
        if self.mode == 'fear':
            self.translateL = self.intensityL * dt
            self.translateR = self.intensityR * dt
        else:
            self.translateR = self.intensityL * dt
            self.translateL = self.intensityR * dt
    
        if self.translateL > self.translateR:
            dx, dy, dtheta = self.turnRightTransformation()
            
        if self.translateL < self.translateR:
            dx, dy, dtheta = self.turnLeftTransformation()
            
        if self.translateL == self.translateR:
            dx, dy = self.rotateVector(0, self.translateL, math.radians(self.rotation))
            dtheta = 0
            
        self.xpos += dx
        self.ypos -= dy
        self.rotation += math.degrees(dtheta)
        
    def turnRightTransformation(self):
        dtheta = (self.translateL - self.translateR)/self.wheel_width
        radius = self.translateR/dtheta + self.wheel_width/2
        dx = radius - math.cos(dtheta)*radius
        dy = math.sin(dtheta)*radius
        dx, dy = self.rotateVector(dx, dy, math.radians(self.rotation))
        return dx, dy, -dtheta

    def turnLeftTransformation(self):
        dtheta = (self.translateR - self.translateL)/self.wheel_width
        radius = self.translateL/dtheta + self.wheel_width/2
        dx = math.cos(dtheta)*radius - radius
        dy = math.sin(dtheta)*radius
        dx, dy = self.rotateVector(dx, dy, math.radians(self.rotation))
        return dx, dy, dtheta
        
    def rotateVector(self, x, y, angle):
        xprime = x*math.cos(angle) - y*math.sin(angle)
        yprime = x*math.sin(angle) + y*math.cos(angle)
        return xprime, yprime
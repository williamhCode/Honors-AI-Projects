#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 18:23:49 2021

@author: williamhou
"""

import math

class bug_1:
    
    def __init__(self, xpos, ypos, rotation, distance):
        self.xpos = xpos
        self.ypos = ypos
        self.rotation = rotation
        self.distance = distance
        
    def sense(self, light_xpos, light_ypos):
        self.sensor_xpos = self.xpos + self.distance * math.cos(math.radians(self.rotation + 90))
        self.sensor_ypos = self.ypos - self.distance * math.sin(math.radians(self.rotation + 90))
        self.light_xpos = light_xpos     
        self.light_ypos = light_ypos
        
        
    def decide(self):
        self.intensity = 30 * 1/((self.sensor_xpos - self.light_xpos)**2 + (self.sensor_ypos - self.light_ypos)**2)**0.5
        
    def act(self, dt):
        self.xpos += self.intensity * math.cos(math.radians(self.rotation + 90)) * dt
        self.ypos -= self.intensity * math.sin(math.radians(self.rotation + 90)) * dt
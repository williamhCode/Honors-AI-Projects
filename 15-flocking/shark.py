#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:08:49 2021

@author: williamhou
"""

import pygame.math
import math

shark_speed = 300
radius = 300
obstacle_radius = 150
dis_to_jaw = 100
jaw_radius = 25
viewAngle = 300

class _shark:
    
    def __init__(self, xpos, ypos, xvec, yvec):
        self.pos = pygame.Vector2(xpos, ypos)
        self.vec = pygame.Vector2(xvec, yvec)
        self.vec.scale_to_length(shark_speed)
        self.angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(self.vec))
        self.jaw_pos = pygame.Vector2(self.pos.x + dis_to_jaw * math.cos(math.radians(self.angle + 90)), self.pos.y + dis_to_jaw * math.sin(math.radians(self.angle + 90)))
        
    def sense(self, boids, obstacles):
        self.boids = boids.copy()
        self.obstacles = obstacles.copy()
        
        i = 0
        while (i < len(self.boids)):
            boid = self.boids[i]
            dis = (self.jaw_pos - boid.pos).length()
            angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(boid.pos - self.jaw_pos))
            angleDiff = self.normalizeAngle((self.angle - angle))
            if(dis > radius or (angleDiff > viewAngle/2 and angleDiff < (360 - viewAngle/2))):
                del self.boids[i]
            else:
                i += 1
    
    def decide(self):
        cohesion = self.computeCohesion(self.boids)
        obstacle = self.avoidObstacle(self.obstacles)
        
        self.vec += cohesion * 20
        self.vec.scale_to_length(shark_speed)
        self.vec += obstacle * 1000
    
    def act(self, dt):
        self.pos += dt * self.vec
        self.angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(self.vec))
        self.jaw_pos = pygame.Vector2(self.pos.x + dis_to_jaw * math.cos(math.radians(self.angle + 90)), self.pos.y + dis_to_jaw * math.sin(math.radians(self.angle + 90)))
    
    def computeCohesion(self, inputList):
        outputVec = pygame.Vector2()
        
        for boid in inputList:
            outputVec += boid.pos
        
        if(outputVec.length() != 0):
             outputVec /= len(inputList)
             outputVec -= self.jaw_pos
             outputVec = outputVec.normalize()
             
        return outputVec
    
    def avoidObstacle(self, inputList):
        outputVec = pygame.Vector2()
        
        for obstacle in inputList:
            angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(obstacle.pos - self.jaw_pos))
            intersect = pygame.Vector2(obstacle.pos.x + obstacle.getRadius() * math.cos(angle), obstacle.pos.y + obstacle.getRadius() * math.sin(angle))
            dis = (intersect - self.jaw_pos).length()
            
            if(dis <= 0):
                outputVec += (self.jaw_pos - obstacle.pos).normalize() / (obstacle.pos - self.jaw_pos).length()
            elif(dis < obstacle_radius):
                outputVec += (self.jaw_pos - intersect).normalize() * (1/dis - 1/(obstacle_radius))
            
        return outputVec
        
    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360
        while (angle >= 360):
            angle -= 360
        return angle
    
    def getRadius(self):
        return radius
    
    def getJawRadius(self):
        return jaw_radius

    def getViewAngle(self):
        return viewAngle
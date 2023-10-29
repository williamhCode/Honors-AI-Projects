#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 10:16:09 2021

@author: williamhou
"""

import pygame.math
import math

#pixels per second
boid_speed = 250
radius = 75
obstacle_radius = 100
viewAngle = 220

class _boid:
    
    def __init__(self, xpos, ypos, xvec, yvec, color):
        self.pos = pygame.Vector2(xpos, ypos)
        self.vec = pygame.Vector2(xvec, yvec)
        self.vec.scale_to_length(boid_speed)
        self.color = color
        self.angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(self.vec))
        
    def sense(self, neighbors, obstacles, sharks):
        self.neighbors = neighbors.copy()
        self.obstacles = obstacles.copy()
        self.sharks = sharks.copy()
        
        i = 0
        while (i < len(self.neighbors)):
            boid = self.neighbors[i]
            dis = (self.pos - boid.pos).length()
            angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(boid.pos - self.pos))
            angleDiff = self.normalizeAngle((self.angle - angle))
            if(dis > radius or dis == 0 or (angleDiff > viewAngle/2 and angleDiff < (360 - viewAngle/2))):
                del self.neighbors[i]
            else:
                i += 1
        
    def decide(self):
        seperation = self.computeSeperation(self.neighbors)
        alignment = self.computeAlignment(self.neighbors)
        cohesion = self.computeCohesion(self.neighbors)
        obstacle = self.avoidObstacle(self.obstacles)
        avoidShark = self.avoidShark(self.sharks)
        
        
        self.vec += seperation * 35
        self.vec += alignment  * 20
        self.vec += cohesion * 30
        self.vec += avoidShark * 80
        self.vec.scale_to_length(boid_speed)
        self.vec += obstacle * 10000
        
    def act(self, dt):
        self.pos += dt * self.vec
        self.angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(self.vec))
    
    def computeCohesion(self, inputList):
        outputVec = pygame.Vector2()
        
        for boid in inputList:
            outputVec += boid.pos
        
        if(outputVec.length() != 0):
             outputVec /= len(inputList)
             outputVec -= self.pos
             outputVec = outputVec.normalize()
             
        return outputVec
    
    def computeSeperation(self, inputList):
        outputVec = pygame.Vector2()
        
        for boid in inputList:
            dis = (self.pos - boid.pos).length()
            if(dis < radius/2):
                outputVec += (self.pos - boid.pos).normalize() / dis
            
        if(outputVec.length() != 0):
            outputVec = outputVec.normalize()
            
        return outputVec

    def computeAlignment(self, inputList):
        outputVec = pygame.Vector2()
        
        for boid in inputList:
            outputVec += boid.vec
           
        if(outputVec.length() != 0):
            outputVec = outputVec.normalize()
            
        return outputVec
    
    def avoidObstacle(self, inputList):
        outputVec = pygame.Vector2()
        
        for obstacle in inputList:
            angle = self.normalizeAngle(pygame.Vector2(0,1).angle_to(obstacle.pos - self.pos))
            intersect = pygame.Vector2(obstacle.pos.x + obstacle.getRadius() * math.cos(angle), obstacle.pos.y + obstacle.getRadius() * math.sin(angle))
            dis = (intersect - self.pos).length()
            
            if(dis <= 0):
                outputVec += (self.pos - obstacle.pos).normalize() / (obstacle.pos - self.pos).length()
            elif(dis < obstacle_radius):
                outputVec += (self.pos - intersect).normalize() * (1/dis - 1/(obstacle_radius))
            
        return outputVec
    
    def avoidShark(self, inputList):
        outputVec = pygame.Vector2()
        
        for shark in inputList:
            dis = (self.pos - shark.jaw_pos).length()
            if(dis < radius):
                outputVec += (self.pos - shark.jaw_pos).normalize() / dis
            
        if(outputVec.length() != 0):
            outputVec = outputVec.normalize()
            
        return outputVec
    
    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360
        while (angle >= 360):
            angle -= 360
        return angle
    
    def getRadius(self):
        return radius
    
    def getViewAngle(self):
        return viewAngle
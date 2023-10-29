#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 10:09:34 2021

@author: williamhou
"""

import pygame
import pygame.gfxdraw
import operator
import math
import random
from boid import _boid
from obstacle import _obstacle
from shark import _shark


def testBounds(obj):
    if obj.pos.x > 1200:
        obj.pos.x = 0
    elif obj.pos.x < 0:
        obj.pos.x = 1200
    elif obj.pos.y > 900:
        obj.pos.y = 0
    elif obj.pos.y < 0:
        obj.pos.y = 900
        
def eatBoids(boidList, sharkList):
    for shark in sharkList:
        i = 0
        while (i < len(boidList)):
            boid = boidList[i]
            dis = (shark.jaw_pos - boid.pos).length()
            if(dis < shark.getJawRadius()):
                del boidList[i]
            else:
                i += 1

def rotateVector(x, y, angle):
    xprime = x*math.cos(angle) - y*math.sin(angle)
    yprime = x*math.sin(angle) + y*math.cos(angle)
    return xprime, yprime

#draw a triangle by its centroid
def drawBoid(screen, xpos, ypos, length, width, angle, color):
    pos = (xpos, ypos)
    angle = math.radians(angle)
    bottom = tuple(map(operator.add, rotateVector(0, length * 2/3, angle), pos))
    right = tuple(map(operator.add, rotateVector(width/2, -length * 1/3, angle), pos))
    left = tuple(map(operator.add, rotateVector(-width/2, -length * 1/3, angle), pos))
    
    pygame.gfxdraw.filled_polygon(screen, (bottom, left, right), color)
    pygame.gfxdraw.aapolygon(screen, (bottom, left, right), color)

def drawObstacle(screen, xpos, ypos, radius, color):
    xpos = int(xpos)
    ypos = int(ypos)
    pygame.gfxdraw.filled_circle(screen, xpos, ypos, radius, color)
    pygame.gfxdraw.aacircle(screen, xpos, ypos, radius, color)
    
def rotateImage(surface, angle, pivot, offset):
    angle *= -1
    rotated_image = pygame.transform.rotozoom(surface, angle, 1)
    rotated_offset = offset.rotate(-angle)
    rect = rotated_image.get_rect(center= pivot+rotated_offset)
    return rotated_image, rect

def showSharkInfo(screen, currShark):
    pygame.draw.circle(screen, (0,0,225), (currShark.jaw_pos.x, currShark.jaw_pos.y), currShark.getJawRadius(), 3)
    pygame.draw.circle(screen, (0,0,225), (currShark.jaw_pos.x, currShark.jaw_pos.y), currShark.getRadius(), 3)
    
    jaw_pos = (currShark.jaw_pos.x, currShark.jaw_pos.y)
    angleLeft = math.radians(currShark.angle + currShark.getViewAngle()/2)
    angleRight = math.radians(currShark.angle - currShark.getViewAngle()/2)
    leftpoint = tuple(map(operator.add, rotateVector(0, currShark.getRadius(), angleLeft), jaw_pos))
    rightpoint = tuple(map(operator.add, rotateVector(0, currShark.getRadius(), angleRight), jaw_pos))
    
    points = [leftpoint, jaw_pos, rightpoint]
    pygame.draw.lines(screen, (0,0,255), False, points, 3)
    
def showBoidInfo(screen, currBoid):
    pygame.draw.circle(screen, (0,0,225), (currBoid.pos.x, currBoid.pos.y), currBoid.getRadius(), 1)
    
    pos = (currBoid.pos.x, currBoid.pos.y)
    angleLeft = math.radians(currBoid.angle + currBoid.getViewAngle()/2)
    angleRight = math.radians(currBoid.angle - currBoid.getViewAngle()/2)
    leftpoint = tuple(map(operator.add, rotateVector(0, currBoid.getRadius(), angleLeft), pos))
    rightpoint = tuple(map(operator.add, rotateVector(0, currBoid.getRadius(), angleRight), pos))
    
    points = [leftpoint, pos, rightpoint]
    pygame.draw.lines(screen, (0,0,255), False, points, 1)
    
def main():
    # screen = pygame.display.set_mode((1200,900), pygame.FULLSCREEN | pygame.SCALED) 
    screen = pygame.display.set_mode((1200,900),0,32)
    pygame.display.set_caption('Flocking Simulation')
    
    boids = []
    obstacles = []
    sharks = []
    
    oceanImg = pygame.image.load('pics/ocean.jpg').convert()
    oceanImg = pygame.transform.smoothscale(oceanImg, (1200,900))
    
    sharksImg = [0] * 17
    i = 0
    while(i < 17):
        name = 'pics/' + str(i+1) + '.png'
        sharkImg = pygame.image.load(name).convert_alpha()
        sharksImg[i] = pygame.transform.scale(sharkImg, (300, 180))
        i += 1
        
    sharks.append(_shark(500, 500, 1, 1))
    
    i = 0
    while(i < 100):
        colorInt = random.randint(30, 100)
        newBoid = _boid(random.randint(0, 1200), random.randint(0, 900), random.random()-0.5, random.random()-0.5, (colorInt,colorInt,colorInt))
        boids.append(newBoid)
        i += 1
    
    # walls
    # i = 0
    # while(i <= 40):
    #     newObstacle = _obstacle(30 * i, 0, (0,0,0))
    #     obstacles.append(newObstacle)
    #     i += 1
    # i = 0
    # while(i <= 40):
    #     newObstacle = _obstacle(30 * i, 900, (0,0,0))
    #     obstacles.append(newObstacle)
    #     i += 1
        
    # i = 0
    # while(i <= 30):
    #     newObstacle = _obstacle(0, 30 * i, (0,0,0))
    #     obstacles.append(newObstacle)
    #     i += 1
    # i = 0
    # while(i <= 30):
    #     newObstacle = _obstacle(1200, 30 * i, (0,0,0))
    #     obstacles.append(newObstacle)
    #     i += 1
    
    font = pygame.font.SysFont('Comic Sans MS', 30)
    
    imgFrame = 0
    
    #Game Loop
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(event.button == 1): 
                    colorInt = random.randint(30, 100)
                    newBoid = _boid(pos[0], pos[1], random.random()-0.5, random.random()-0.5, (colorInt, colorInt, colorInt))
                    boids.append(newBoid)
                if(event.button == 3):
                    newObstacle = _obstacle(pos[0], pos[1], (0,0,0))
                    obstacles.append(newObstacle)


        dt = clock.tick(60)/1000
        screen.fill((50,50,50))
        
        screen.blit(oceanImg, (0,0))
        
        for boid in boids:
            boid.sense(boids, obstacles, sharks)
        for shark in sharks:
            shark.sense(boids, obstacles)
            
        for boid in boids:
            boid.decide()
        for shark in sharks:
            shark.decide()
            
        for boid in boids:
            boid.act(dt)
            testBounds(boid)
            
        for shark in sharks:
            shark.act(dt)
            testBounds(shark)
        
        for obstacle in obstacles:
            drawObstacle(screen, obstacle.pos.x, obstacle.pos.y, obstacle.getRadius(), obstacle.color)
            
        imgFrame += 0.3
        if(imgFrame > 17):
            imgFrame = 0
            
        i = 0
        while(i < len(sharks)):
            currShark = sharks[i]
            currImg = sharksImg[int(imgFrame)]
            sharkImg_copy, sharkImg_copy_rect = rotateImage(currImg, currShark.angle + 90, [currShark.pos.x,currShark.pos.y], pygame.math.Vector2(0,0))
            screen.blit(sharkImg_copy, sharkImg_copy_rect)
            
            # showSharkInfo(screen, currShark)
            i += 1
            
        for boid in boids:
            drawBoid(screen, boid.pos.x, boid.pos.y, 12, 8, boid.angle, boid.color)
            # showBoidInfo(screen, boid)
        
        boidNumber = font.render('Boid Count: ' + str(len(boids)), False, (50,50,50))
        
        screen.blit(boidNumber, (950, 850))
        
        eatBoids(boids, sharks)
        
        pygame.display.update()
    
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()
    pygame.quit()
    

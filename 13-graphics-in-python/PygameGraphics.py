#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:48:53 2021

@author: williamhou
"""

import pygame

#Initialize pygame
pygame.init()


#SetupWindow
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption('Pygame Graphics')


grassImg = pygame.image.load('grass.jpeg')
grassImg = pygame.transform.scale(grassImg, (800,600))
ballImg = pygame.image.load('ball.png')
ballImg = pygame.transform.smoothscale(ballImg, (100,100))
ballX = 200
ballY = 200
ballSpeedX = 1.3
ballSpeedY = 2.2
dt = 0

def changeball():
    
    global ballX
    global ballY
    global ballSpeedX
    global ballSpeedY
    
    ballX += ballSpeedX * dt / 5
    ballY += ballSpeedY * dt / 5
    
    if(ballX < -5 or ballX > 705):
        ballSpeedX *= -1
        
    if(ballY < -5 or ballY > 505):
        ballSpeedY *= -1
    
    screen.blit(ballImg,(ballX, ballY))
    

#Game Loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((100,0,0))
    
    dt = clock.tick(60)
    
    screen.blit(grassImg,(0, 0))
    changeball()
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()
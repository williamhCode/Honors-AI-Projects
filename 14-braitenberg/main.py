#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 18:22:36 2021

@author: williamhou
"""

import pygame
from bug1 import bug_1
from bug2 import bug_2
from light import light_

# https://www.youtube.com/watch?v=4_9twnEduFA
class button():
    def __init__(self, color, x, y, width, height, text= '', font= ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self, win, outline= None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            if self.font == '':
                font = pygame.font.SysFont('comicsans', 60)
            else:
                font = self.font
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# https://stackoverflow.com/questions/15098900/how-to-set-the-pivot-point-center-of-rotation-for-pygame-transform-rotate
def rotate(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotozoom(surface, angle, 1)
    rotated_offset = offset.rotate(-angle)
    rect = rotated_image.get_rect(center= pivot+rotated_offset)
    return rotated_image, rect

def testBounds(obj, objImgRect):
    inBounds = pygame.Rect(0, 0, 1200, 900).colliderect(objImgRect)
    if not inBounds:
        if obj.xpos > 1200:
            obj.xpos = 0
        elif obj.xpos < 0:
            obj.xpos = 1200
        elif obj.ypos > 900:
            obj.ypos = 0
        elif obj.ypos < 0:
            obj.ypos = 900
            
def cursorInvis(invis):
    if invis:
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
def showPositions(screen, vehicle):
    pygame.draw.circle(screen, (0,0,225), (vehicle.wheelL_xpos,vehicle.wheelL_ypos),5)
    pygame.draw.circle(screen, (0,0,225), (vehicle.wheelR_xpos,vehicle.wheelR_ypos),5)
    pygame.draw.circle(screen, (225,225,225), (vehicle.xpos,vehicle.ypos),5)
            
    pygame.draw.circle(screen, (225,0,0), (vehicle.sensorL_xpos,vehicle.sensorL_ypos),5)
    pygame.draw.circle(screen, (225,0,0), (vehicle.sensorR_xpos,vehicle.sensorR_ypos),5)
            
def main():
    #SetupWindow
    screen = pygame.display.set_mode((1200,900))
    pygame.display.set_caption('Bug Simulation')

    bugImg = pygame.image.load('pic/bug.png').convert_alpha()
    bugImg = pygame.transform.smoothscale(bugImg, (120,160))
    bug1 = bug_1(0,450,-90, bugImg.get_height())
    bug2 = bug_2(300,500,0, bugImg.get_height(), bugImg.get_width()*0.84, bugImg.get_width()/2, 'fear')
    bug3 = bug_2(300,500,0, bugImg.get_height(), bugImg.get_width()*0.84, bugImg.get_width()/2, 'aggro')
    
    lightImg = pygame.image.load('pic/light.png').convert_alpha()
    lightImg = pygame.transform.scale(lightImg, (300,300))
    light = light_(1000, 400)
    
    button1 = button((100,100,100),200,300,200,100,'Basic Bug',pygame.font.SysFont('comicsans', 35))
    button2 = button((100,100,100),500,300,200,100,'Fearful Bug',pygame.font.SysFont('comicsans', 35))
    button3 = button((100,100,100),800,300,200,100,'Aggro Bug',pygame.font.SysFont('comicsans', 35))
    buttonX = button((100,100,100),0,0,30,30,'X',pygame.font.SysFont('Arial', 20))
    
    #Game Loop
    mode = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.MOUSEMOTION:
                if buttonX.isOver(pos):
                    cursorInvis(False)
                elif mode != 0:
                    cursorInvis(True)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 0:
                    if button1.isOver(pos):
                        mode = 1
                        bug1.xpos = 0
                        bug1.ypos = 450
                        cursorInvis(True)
                    if button2.isOver(pos):
                        mode = 2
                        bug2.xpos = 300
                        bug2.ypos = 500
                        bug2.rotation = 0
                        cursorInvis(True)
                    if button3.isOver(pos):
                        mode = 3
                        bug3.xpos = 300
                        bug3.ypos = 500
                        bug3.rotation = 0
                        cursorInvis(True)
                else:
                    if buttonX.isOver(pos):
                        mode = 0
        
        if mode != 0:
            dt = clock.tick(60)
            light.xpos, light.ypos = pos
            screen.fill((0,0,0))
            
            lightImg_rect = lightImg.get_rect(center= (light.xpos, light.ypos))
            screen.blit(lightImg, lightImg_rect)
            
        
        if mode == 0:
            screen.fill((225,225,225))
            button1.draw(screen,(0,0,0))
            button2.draw(screen,(0,0,0))
            button3.draw(screen,(0,0,0))
            
        elif mode == 1:
            bug1.sense(light.xpos, light.ypos)
            bug1.decide()
            bug1.act(dt)
            
            bugImg1_copy, bugImg1_copy_rect = rotate(bugImg, bug1.rotation, [bug1.xpos,bug1.ypos], pygame.math.Vector2(0,-bugImg.get_height()/2))
            screen.blit(bugImg1_copy, bugImg1_copy_rect)
            
            testBounds(bug1, bugImg1_copy_rect)
            
        elif mode == 2:
            bug2.sense(light.xpos, light.ypos)
            bug2.decide()
            bug2.act(dt)
            
            bugImg2_copy, bugImg2_copy_rect = rotate(bugImg, bug2.rotation, [bug2.xpos,bug2.ypos], pygame.math.Vector2(0,-bugImg.get_height()/2))
            screen.blit(bugImg2_copy, bugImg2_copy_rect)
            
            # showPositions(screen, bug2)
            
            testBounds(bug2, bugImg2_copy_rect)
            
        elif mode == 3:     
            bug3.sense(light.xpos, light.ypos)
            bug3.decide()
            bug3.act(dt)
            
            bugImg3_copy, bugImg3_copy_rect = rotate(bugImg, bug3.rotation, [bug3.xpos,bug3.ypos], pygame.math.Vector2(0,-bugImg.get_height()/2))
            screen.blit(bugImg3_copy, bugImg3_copy_rect)
            
            # showPositions(screen, bug3)
        
            testBounds(bug3, bugImg3_copy_rect)
            
        if mode != 0:
            buttonX.draw(screen)
            
            
        pygame.display.update()
        
    
if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
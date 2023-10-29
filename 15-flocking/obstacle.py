#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 09:18:37 2021

@author: williamhou
"""

import pygame.math

radius = 25

class _obstacle:
    
    def __init__(self, xpos, ypos, color):
         self.pos = pygame.Vector2(xpos, ypos)
         self.color = color
         
    def getRadius(self):
        return radius
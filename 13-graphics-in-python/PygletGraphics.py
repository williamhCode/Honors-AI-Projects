#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 09:25:55 2021

@author: williamhou
"""

import pyglet
import pyglet.window.key as key

win = pyglet.window.Window(width = 800, height = 600)

ballImg = pyglet.image.load('ball.png') 
sprite = pyglet.sprite.Sprite(ballImg, x = ballImg.width//2, y = win.height//2 )
value = sprite.scale = 0.2

@win.event
def on_key_press(key, modifiers):
    
    if (key == pyglet.window.key.LEFT):
        sprite.x -= 20
    if(key == pyglet.window.key.RIGHT):
        sprite.x += 20
        
    if (key == pyglet.window.key.UP):
        sprite.y += 20
    if (key == pyglet.window.key.DOWN):
        sprite.y -= 20

@win.event
def on_draw():
    win.clear()
    sprite.draw()
        
pyglet.app.run()


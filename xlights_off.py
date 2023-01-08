#!/bin/python3
import board
import neopixel

# variables
no_of_lights=200

pixels = neopixel.NeoPixel(board.D18, no_of_lights, auto_write=False)
for i in range(no_of_lights):
   pixels[i]= [0,0,0]

pixels.show()

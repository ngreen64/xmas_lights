#!/bin/python3
import board
import neopixel
import time
import random
import math
from pprint import pprint
from time import sleep
import sys
import xlights_common_vars as com_var
import xlights_common_functions as com_func

# Instantiate pixel library
pixels = neopixel.NeoPixel(board.D18, com_var.no_of_lights, auto_write=False)
           
# Time variables - i.e. not module specific
timelast=com_func.current_milli_time()
start_time=timelast
last_random_change=start_time

def do_randomisation(timenow):
      # Change settings at random. Wait between 10-30 seconds between changes before changing again.
      global last_random_change
      global lights_at_a_time_new
      global lights_at_a_time
      global time_for_run_new
      global time_for_run
      global default_light_falloff_new
      global default_light_falloff
      global direction
      global bidirectional
      global gap_between_lights_ms
      if com_var.fade_status == "fade" and com_var.fade_factor == 0:
         print("Now I triggered")
         last_random_change = timenow
        
         if random.randint(1,100) > 25:
           time_for_run_new = random.randint(250,25000)/1000
           #print("Random chan/10000ge. Set light run time from " + str(time_for_run) + " to " + str(time_for_run_new))
           time_for_run = time_for_run_new
         if random.randint(1,100) > 25:
           lights_at_a_time_new = random.randint(1,round(com_var.no_of_lights/10))
           if lights_at_a_time_new != lights_at_a_time:
              #print("Random change. Set lights at a time from " + str(lights_at_a_time) + " to " + str(lights_at_a_time_new))
              lights_at_a_time = lights_at_a_time_new
         if random.randint(1,100) > 50:
           if random.randint(1,100) > 50:
              default_light_falloff_new = random.uniform(1,round(com_var.no_of_lights/5))
           else:
              default_light_falloff_new = str(random.uniform(1,round(com_var.no_of_lights/5))) + "-" + str(random.uniform(1,round(com_var.no_of_lights/5)))
           if default_light_falloff_new != default_light_falloff:
              #print("Random change. Default light falloff changed from " + str(default_light_falloff) + " to " + str(default_light_falloff_new))
              default_light_falloff = default_light_falloff_new
         if random.randint(1,100) > 50:
           direction_new = "negative"
         else:
           direction_new = "positive"
         if direction_new != direction:
           #print("Random change. Direction changed from " + str(direction) + " to " + str(direction_new))
           direction = direction_new
         if random.randint(1,100) > 50:
           bidirectional_new = "y"
         else:
           bidirectional_new = "n"
         if bidirectional_new != bidirectional:
           #print("Random change. Bidirectional boolean changed from " + str(bidirectional) + " to " + str(bidirectional_new))
           bidirectional = bidirectional_new
         gap_between_lights_ms=gap_between_lights()
         com_var.fade_status="unfade"
      elif timenow > last_random_change + com_var.rand_change_time*1000: # It's time to randomise
         if com_var.fade_status == "none":
            print("triggering")
            com_var.fade_status="fade"
            com_var.fade_start_time = timenow
      
# Import light pattern modules
#sys.path.append('./xlights_smooth_modules')
#from smooth_with_random_changes import *

def gap_between_lights():
    #print("Gap between lights needs to be " + str((time_for_run*1000)/lights_at_a_time))
    return (time_for_run*1000)/lights_at_a_time

def calc_intensity_values(position_diff,light_span):
    return 1-((position_diff/light_span)**2)**0.5

def calculate_light(light_dir):
    global x
    if light_dir == "backward":
       while 0 <= x <= com_var.no_of_lights - 1 + light_span:
            pos_delta = position - x
            if position - pos_delta >= com_var.no_of_lights:
               x-=1
               continue
            if pos_delta > light_span:
               break
            intensity = calc_intensity_values(pos_delta,light_span)
            bulb_no = round(position - pos_delta)
            light_values_next[bulb_no] = [ colours_in_play[colour_time][0]*intensity, colours_in_play[colour_time][1]*intensity, colours_in_play[colour_time][2]*intensity ]
            if light_values_now[bulb_no] == [0,0,0]:
               light_values_now[bulb_no] = light_values_next[bulb_no]
            else:
               for p in range(3):
                   if light_values_next[bulb_no][p] > light_values_now[bulb_no][p]:
                      light_values_now[bulb_no][p] = light_values_next[bulb_no][p]
            x-=1
    if light_dir == "forward":
       while 0 - light_span <= x <= com_var.no_of_lights - 1:
            pos_delta = x - position
            if position + pos_delta < 0:
               x+=1
               continue
            if pos_delta > light_span:
               break
            intensity = calc_intensity_values(pos_delta,light_span)
            bulb_no = round(position + pos_delta)
            light_values_next[bulb_no] = [ colours_in_play[colour_time][0]*intensity, colours_in_play[colour_time][1]*intensity, colours_in_play[colour_time][2]*intensity ]
            if light_values_now[bulb_no] == [0,0,0]:
               light_values_now[bulb_no] = light_values_next[bulb_no]
            else:
               for p in range(3):
                   if light_values_next[bulb_no][p] > light_values_now[bulb_no][p]:
                      light_values_now[bulb_no][p] = light_values_next[bulb_no][p]
            x+=1
            
##### Last change on 15th of October. Trying to break out the modules into separate files. Error on variables in those files that I need to solve

############################# Specific module vars start ####################################
time_for_run=30
lights_at_a_time=1
direction="positive"
bidirectional="y"
default_light_falloff=1.0 # This can either be an integer e.g. 6, or declared as a string for a range e.g. "6-10". Set 1 or higher!
current_gap=0
gap_between_lights_ms=gap_between_lights()
default_light_falloff_new = default_light_falloff
lights_at_a_time_new = lights_at_a_time
time_for_run_new = time_for_run
############################# Specific module vars end ####################################


# Calculate position and intensity of lights 
light_values_now = {}
colours_in_play = {}
light_values_next = {}

fps=0
fps_count=com_func.current_milli_time()
frames=0
    
# All variables pre-set now let's loop...
while True:
   loop_time=com_func.current_milli_time()
   timenow=loop_time
   frames += 1
   
   # Prints the Frames per second every 5 seconds
   if loop_time >= fps_count + 5000:
       print("FPS = " + str(int(frames / ((loop_time - fps_count)/1000))))
       frames = 0
       fps_count = loop_time

   # Blank out the pixel array so that everything can be recalculated this loop
   for i in range(com_var.no_of_lights):
       light_values_now[i]= [0,0,0]

   # Calculate the current time gap since
   t_delta = timenow - timelast

   # Calculate fading for random transition
   if com_var.randomise == "y":
      com_func.set_fade_factor(timenow,last_random_change)
      
############################# Specific module start ####################################

   if com_var.first_run == "yes":
      if isinstance(default_light_falloff, float):
         colours_in_play[timenow] = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
      else:
         colours_in_play[timenow] = com_func.give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)

   # Insert a new colour should the gap be big enough and reset gap timer
   if t_delta >= gap_between_lights_ms:
     timelast = timenow
     if isinstance(default_light_falloff, float):
         colours_in_play[timenow] = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
     else:
         colours_in_play[timenow] = com_func.give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)
     # Unsure of why the following check on randomise is here. See what happens when this is removed
     if com_var.randomise == "n":
         if direction == "positive" and bidirectional == "y":
             direction = "negative"
         else:
             direction = "positive"

   # Work through the dictionary and calculate the affect of the colour on the lights in the chain
   for colour_time in list(colours_in_play):
     light_span = colours_in_play[colour_time][4]
     this_light_time_for_run = colours_in_play[colour_time][5]

     for i in range(com_var.no_of_lights):
         light_values_next[i]= [0,0,0]

     if colours_in_play[colour_time][3] == "positive":
        position = ((timenow - colour_time)/1000)/this_light_time_for_run*(com_var.no_of_lights+light_span*2) - light_span
        if position > com_var.no_of_lights + light_span:
          colours_in_play.pop(colour_time)
          continue

     if colours_in_play[colour_time][3] == "negative":
        position = com_var.no_of_lights - 1 - ((timenow - colour_time)/1000)/this_light_time_for_run*(com_var.no_of_lights+light_span*2) + light_span
        if position < light_span*-1:
          colours_in_play.pop(colour_time)
          continue


     # Calculate the light on the bulbs in its influence
     closest_low_pos = math.floor(position)
     x = closest_low_pos
     # First calculate backwards...
     calculate_light("backward")
     x = closest_low_pos + 1
     # then light forwards...
     calculate_light("forward")
     
############################# Specific module end ####################################

   for item in light_values_now:
        try:
            pixels[item] = [light_values_now[item][0]*com_var.fade_factor, light_values_now[item][1]*com_var.fade_factor, light_values_now[item][2]*com_var.fade_factor]
        except Exception as e:
            pprint(light_values_now)
            pprint(colours_in_play)
            print(e)
            sys.exit()

   pixels.show()

   if com_var.randomise == "y":
      do_randomisation(timenow)
   if com_var.first_run == "yes":
      com_var.first_run="no"

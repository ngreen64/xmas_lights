#!/bin/python3
import board
import neopixel
import time
import random
import math
from pprint import pprint
from time import sleep
import sys

# Version 2
# Modify the way that the light is calculated. Instead of forward and back light numbers,
# have two possible equations for messuring light ahead and behind. Work against a dictionary
# and add values to it based on the light equations.

# g,r,b
def current_milli_time():
    return round(time.time() * 1000)

def give_me_a_colour(direction,light_falloff,time_for_run):
    a = 0
    b = 0 
    c = 0
    while a + b + c < 40:
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
    return (a,b,c,direction,light_falloff,time_for_run)

def gap_between_lights():
    print("Gap between lights needs to be " + str((time_for_run*1000)/lights_at_a_time))
    return (time_for_run*1000)/lights_at_a_time

def calc_intensity_values(position_diff,light_span):
#    return 1-(position_diff/light_span)**2
    return 1-((position_diff/light_span)**2)**0.5

def set_fade_factor(timenow,last_random_change):
     global randomise
     global fade_status
     global fade_factor
     if randomise == "y" and fade_status == "fade":
        fade_factor = 1-(timenow-last_random_change)/1000
        if fade_factor < 0.005:
            fade_factor = 0
            randomised = "yes"
     elif randomise == "y" and fade_status == "unfade" :
        fade_factor = (timenow-last_random_change)/1000
        if fade_factor >= 1:
            fade_factor=1
            fade_status="none"
     else:
         fade_factor=1

def do_randomisation(timenow):
   if randomise == "y":
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
       global fade_status
       global ramdomised
       global gap_between_lights_ms
       if timenow > last_random_change + rand_change_time*1000: # 10 seconds has elapsed since last random change or the start of the script
           last_random_change = timenow
           if random.randint(1,100) > 25:
              time_for_run_new = random.randint(250,25000)/1000
              print("Random change. Set light run time from " + str(time_for_run) + " to " + str(time_for_run_new))
              time_for_run = time_for_run_new
           if random.randint(1,100) > 25:
              lights_at_a_time_new = random.randint(1,round(no_of_lights/10))
              if lights_at_a_time_new != lights_at_a_time:
                 print("Random change. Set lights at a time from " + str(lights_at_a_time) + " to " + str(lights_at_a_time_new))
                 lights_at_a_time = lights_at_a_time_new
           if random.randint(1,100) > 50:
              if random.randint(1,100) > 50:
                 default_light_falloff_new = random.uniform(1,round(no_of_lights/5))
              else:
                 default_light_falloff_new = str(random.uniform(1,round(no_of_lights/5))) + "-" + str(random.uniform(1,round(no_of_lights/5)))
              if default_light_falloff_new != default_light_falloff:
                 print("Random change. Default light falloff changed from " + str(default_light_falloff) + " to " + str(default_light_falloff_new))
                 default_light_falloff = default_light_falloff_new
           if random.randint(1,100) > 50:
              direction_new = "negative"
           else:
              direction_new = "positive"
           if direction_new != direction:
              print("Random change. Direction changed from " + str(direction) + " to " + str(direction_new))
              direction = direction_new
           if random.randint(1,100) > 50:
              bidirectional_new = "y"
           else:
              bidirectional_new = "n"
           if bidirectional_new != bidirectional:
              print("Random change. Bidirectional boolean changed from " + str(bidirectional) + " to " + str(bidirectional_new))
              bidirectional = bidirectional_new
           gap_between_lights_ms=gap_between_lights()


def calculate_light(light_dir):
    global x
    if light_dir == "backward":
       while 0 <= x <= no_of_lights - 1 + light_span:
            pos_delta = position - x
            if position - pos_delta >= no_of_lights:
               x-=1
               continue
            if pos_delta > light_span:
               break
            intensity = calc_intensity_values(pos_delta,light_span)
            bulb_no = round(position - pos_delta)
            light_values_next[bulb_no] = [ colours_in_play[colour_time][0]*intensity*fade_factor, colours_in_play[colour_time][1]*intensity*fade_factor, colours_in_play[colour_time][2]*intensity*fade_factor ]
            if light_values_now[bulb_no] == [0,0,0]:
               light_values_now[bulb_no] = light_values_next[bulb_no]
            else:
               for p in range(3):
                   if light_values_next[bulb_no][p] > light_values_now[bulb_no][p]:
                      light_values_now[bulb_no][p] = light_values_next[bulb_no][p]
            x-=1
    if light_dir == "forward":
       while 0 - light_span <= x <= no_of_lights - 1:
            pos_delta = x - position
            if position + pos_delta < 0:
               x+=1
               continue
            if pos_delta > light_span:
               break
            intensity = calc_intensity_values(pos_delta,light_span)
            bulb_no = round(position + pos_delta)
            light_values_next[bulb_no] = [ colours_in_play[colour_time][0]*intensity*fade_factor, colours_in_play[colour_time][1]*intensity*fade_factor, colours_in_play[colour_time][2]*intensity*fade_factor ]
            if light_values_now[bulb_no] == [0,0,0]:
               light_values_now[bulb_no] = light_values_next[bulb_no]
            else:
               for p in range(3):
                   if light_values_next[bulb_no][p] > light_values_now[bulb_no][p]:
                      light_values_now[bulb_no][p] = light_values_next[bulb_no][p]
            x+=1

# variables
no_of_lights=100
time_for_run=30
lights_at_a_time=1
timelast=current_milli_time()
default_light_falloff=1.0 # This can either be an integer e.g. 6, or declared as a string for a range e.g. "6-10". Set 1 or higher!
current_gap=0
gap_between_lights_ms=gap_between_lights()
start_time=timelast
direction="positive"

bidirectional="y"
randomise="y"
rand_change_time=20 # Set the initial random change time to 1 minute
max_rand_change_time=30

# Do not change these
pixels = neopixel.NeoPixel(board.D18, no_of_lights, auto_write=False)
last_random_change=start_time
randomised="no"
time_for_run_new = time_for_run
lights_at_a_time_new = lights_at_a_time
default_light_falloff_new = default_light_falloff
fade_status="none"
fade_factor=1

# Calculate position and intensity of lights forward and backward 
light_values_now = {}
colours_in_play = {}
light_values_next = {}

fps=0
fps_count=current_milli_time()
frames=0

if isinstance(default_light_falloff, float):
    colours_in_play[fps_count] = give_me_a_colour(direction,default_light_falloff,time_for_run)
else:
    colours_in_play[fps_count] = give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)

while True:
   loop_time=current_milli_time()
   frames += 1
   if loop_time >= fps_count + 5000:
       print("FPS = " + str(int(frames / ((loop_time - fps_count)/1000))))
       frames = 0
       fps_count = loop_time

   for i in range(no_of_lights):
       light_values_now[i]= [0,0,0]

   timenow=current_milli_time()
   # Calculate the current gap
   t_delta = timenow - timelast

   # Insert a new colour should the gap be big enough and reset gap timer
   if t_delta >= gap_between_lights_ms:
     timelast = timenow
     if isinstance(default_light_falloff, float):
         colours_in_play[timenow] = give_me_a_colour(direction,default_light_falloff,time_for_run)
     else:
         colours_in_play[timenow] = give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)
     if randomise == "n":
         if direction == "positive" and bidirectional == "y":
             direction = "negative"
         else:
             direction = "positive"

   # Work through the dictionary and calculate the affect of the colour on the lights in the chain
   for colour_time in list(colours_in_play):
     light_span = colours_in_play[colour_time][4]
     this_light_time_for_run = colours_in_play[colour_time][5]

     for i in range(no_of_lights):
         light_values_next[i]= [0,0,0]

     if colours_in_play[colour_time][3] == "positive":
        position = ((timenow - colour_time)/1000)/this_light_time_for_run*(no_of_lights+light_span*2) - light_span
        if position > no_of_lights + light_span:
          colours_in_play.pop(colour_time)
          continue

     if colours_in_play[colour_time][3] == "negative":
        position = no_of_lights - 1 - ((timenow - colour_time)/1000)/this_light_time_for_run*(no_of_lights+light_span*2) + light_span
        if position < light_span*-1:
          colours_in_play.pop(colour_time)
          continue

     # Calculate fading for random transition
     set_fade_factor(timenow,last_random_change)

     # Calculate the light on the bulbs in its influence
     closest_low_pos = math.floor(position)
     x = closest_low_pos
     # First calculate backwards...
     calculate_light("backward")
     x = closest_low_pos + 1
     # then light forwards...
     calculate_light("forward")

   for item in light_values_now:
        try:
            pixels[item] = light_values_now[item]
        except:
            pprint(light_values_now)
            pprint(colours_in_play)
            sys.exit()

   pixels.show()
#   pprint(light_values_now)
#   for i in range(0,10):
#       print(str(i) + " " + str(light_values_now[i][0] + light_values_now[i][1] + light_values_now[i][2]))
#   pprint(colours_in_play)
#   sys.exit()

   do_randomisation(timenow)

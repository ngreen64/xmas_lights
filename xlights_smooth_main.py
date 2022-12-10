#!/bin/python3
import board
import neopixel
import random
import math
from pprint import pprint
from time import sleep
import sys
import importlib
import xlights_common_vars as com_var
import xlights_common_functions as com_func

# Instantiate pixel library and set the bulb variables to off initially
pixels = neopixel.NeoPixel(board.D18, com_var.no_of_lights, auto_write=False)

for i in range(com_var.no_of_lights):
    com_var.light_values_now[i]= [0,0,0]
           
# Time variables - i.e. not module specific
timelast=com_func.current_milli_time()
start_time=timelast
com_var.last_random_change=start_time
com_var.last_random_module_change=start_time

# List modules
sys.path.append(com_var.mods_dir)
available_modules = com_func.list_modules(com_var.mods_dir)
module_in_use = ""

def select_a_random_module():
   global module_in_use
   global available_modules
   global current_module
   try: current_module
   except:
      module_in_use = random.choice(available_modules)
      print("Selecting module " + module_in_use)
      current_module = importlib.import_module(module_in_use, package=None)
   else:
      del sys.modules[module_in_use]
      del module_in_use
      module_in_use = random.choice(available_modules)
      print("Unloading module and now selecting module " + module_in_use)
      current_module = importlib.import_module(module_in_use, package=None)

try: 
   print("Trying to launch " + str(sys.argv[1]))
   current_module = importlib.import_module(sys.argv[1], package=None)
except Exception as e:
   print(e)
   select_a_random_module()
   com_var.randomise_modules="y"

fps=0
fps_count=com_func.current_milli_time()
frames=0
    
# All variables pre-set now let's loop...
while True:
   loop_time=com_func.current_milli_time()
   com_var.timenow=loop_time
   frames += 1
   
   # Prints the Frames per second every 5 seconds
   if loop_time >= fps_count + 5000:
       print("FPS = " + str(int(frames / ((loop_time - fps_count)/1000))))
       frames = 0
       fps_count = loop_time

   # Calculate the current time gap since
   com_var.t_delta = com_var.timenow - com_var.timelast

   # Calculate fading for random module transition
   if com_var.randomise_modules == "y":
      if com_var.fade_status == "complete":
         com_var.last_random_module_change = com_var.timenow
         com_var.fade_status = "none"
      if com_var.fade_factor == 0:
         if com_var.fade_status != "unfade":
            com_var.fade_status = "unfade"
            com_var.fade_start_time = com_var.timenow
            print("####################################################################")
            current_module.close_out_module()
            select_a_random_module()
            current_module.run_once_at_start()
         com_func.set_fade_factor(com_var.timenow,com_var.last_random_module_change)
      if com_var.timenow > com_var.last_random_module_change + com_var.rand_module_change_time*1000:
         if com_var.fade_status == "none":
            com_var.fade_status = "fade"
            com_var.fade_start_time = com_var.timenow
         com_func.set_fade_factor(com_var.timenow,com_var.last_random_module_change)
   
   if com_var.first_run == "yes":
      current_module.run_once_at_start()

   
   current_module.run_each_loop()
 
   for item in com_var.light_values_now:
        try:
            pixels[item] = [com_var.light_values_now[item][0]*com_var.fade_factor, com_var.light_values_now[item][1]*com_var.fade_factor, com_var.light_values_now[item][2]*com_var.fade_factor]
        except Exception as e:
            pprint(com_var.light_values_now)
            print(e)
            sys.exit()
            
   pixels.show()

   if com_var.first_run == "yes":
      com_var.first_run="no"

import time
import random
import sys
from os import listdir
from os.path import isfile, join
import xlights_common_vars as com_var

def current_milli_time():
    return round(time.time() * 1000)
    
def blank_array():
   # Blank out the pixel array so that everything can be recalculated this loop
   for i in range(com_var.no_of_lights):
       com_var.light_values_now[i]= [0,0,0]
    
def give_me_a_colour(direction,light_falloff,time_for_run):
    a = 0
    b = 0 
    c = 0
    while a + b + c < 40:
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
    return (a,b,c,direction,light_falloff,time_for_run) 

def set_fade_factor(timenow,last_random_change):
    if com_var.fade_status == "fade":
        com_var.fade_factor = 1-(timenow-com_var.fade_start_time)/com_var.fading_time_ms
        if com_var.fade_factor < 0.005:
           com_var.fade_factor=0
           print("Fading complete")
    elif com_var.fade_status == "unfade":
        com_var.fade_factor = (timenow-com_var.fade_start_time)/com_var.fading_time_ms
        if com_var.fade_factor >= 1:
           com_var.fade_factor=1
           com_var.fade_status="complete"
           print("Unfading complete")

def list_modules(mods_dir):
	files = listdir(mods_dir)
	found_modules = []
	for i in files:
		if isfile(join(mods_dir, i)) and i[-3:] == ".py" and i != "__init__.py":
			found_modules.append(i[:-3])
	return(found_modules)
	
def fade_lit_pixels(fade_amount):
    for i in range(com_var.no_of_lights):
       if com_var.light_values_now[i][0] > 0:
           if com_var.light_values_now[i][0] >= fade_amount:
              com_var.light_values_now[i][0] = com_var.light_values_now[i][0] - fade_amount
           else:
              com_var.light_values_now[i][0] = 0
       if com_var.light_values_now[i][1] > 0:
           if com_var.light_values_now[i][1] >= fade_amount:
              com_var.light_values_now[i][1] = com_var.light_values_now[i][1] - fade_amount
           else:
              com_var.light_values_now[i][1] = 0
       if com_var.light_values_now[i][2] > 0:
           if com_var.light_values_now[i][2] >= fade_amount:
              com_var.light_values_now[i][2] = com_var.light_values_now[i][2] - fade_amount
           else:
              com_var.light_values_now[i][2] = 0

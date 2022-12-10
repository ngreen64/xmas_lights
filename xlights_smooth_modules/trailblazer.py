import xlights_common_vars as com_var
import xlights_common_functions as com_func
import random
import math

############################# Specific module vars start ####################################
direction="positive"
bidirectional="y"
default_light_falloff=1.0 # This can either be an integer e.g. 6, or declared as a string for a range e.g. "6-10". Set 1 or higher!
current_gap=0
gap_between_lights_ms=0
default_light_falloff_new = default_light_falloff
last_light_released=0
colours_in_play = {}
time_for_run=5
acceleration=0
############################# Specific module vars end ####################################

def calc_acceleration():
   global time_for_run
   global acceleration
   acceleration = (2*com_var.no_of_lights)/time_for_run**2

def run_once_at_start():
   com_func.blank_array()
   randomise_vars()
   calc_acceleration()
   print("Start time " + str(com_var.timenow))
   
def randomise_vars():
   global gap_between_lights_ms
   global direction
   global time_for_run
   if random.randint(1,5) == 1:
      direction = "positive"
   else:
      direction = "negative"
   gap_between_lights_ms = math.ceil(random.randint(1,5)*com_var.no_of_lights/100)*1000
   time_for_run = random.randint(3,10)

def close_out_module():
   print("Closing module")

def run_each_loop():
   global direction
   global colours_in_play
   global last_light_released
   global time_for_run
   if com_var.timenow > last_light_released + gap_between_lights_ms:
      colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,0,time_for_run)
      last_light_released = com_var.timenow
      randomise_vars()
   com_func.fade_lit_pixels(0.5)

   for colour_time in list(colours_in_play):
      this_light_time_for_run = colours_in_play[colour_time][5]

      if colours_in_play[colour_time][3] == "positive":
         position = math.floor(0.5*acceleration*((com_var.timenow - colour_time)/1000)**2)
         if position > com_var.no_of_lights-1:
           colours_in_play.pop(colour_time)
           continue
         
      if colours_in_play[colour_time][3] == "negative":
         position = math.ceil(com_var.no_of_lights - 1 - math.floor(0.5*acceleration*((com_var.timenow - colour_time)/1000)**2))
         if position < 0:
           colours_in_play.pop(colour_time)
           continue
      
      com_var.light_values_now[position] = [ colours_in_play[colour_time][0] , colours_in_play[colour_time][1] ,colours_in_play[colour_time][2] ]

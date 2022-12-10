import xlights_common_vars as com_var
import xlights_common_functions as com_func
import random
from time import sleep
# Insert any other python modules required here

############################# Specific module vars start ####################################
# Insert any specific module variables here
colour1 = com_func.give_me_a_colour("",0,0)
colour2 = com_func.give_me_a_colour("",0,0)
colour3 = com_func.give_me_a_colour("",0,0)
last_bulb_change = 0
time_between_bulb_changes_ms=random.randint(5,125)
current_bulb=0
############################# Specific module vars end ######################################

############################# Specific module functions start ####################################
# Define any specific module functions here
############################# Specific module functions end ######################################

def run_once_at_start():
   global last_bulb_change
   # Called just when the module is initialised this function should set up anything done first 
   # time into the module
   print("Starting module")
   com_func.blank_array()
   com_var.light_values_now[0] = [ colour1[0], colour1[1], colour1[2] ]
   last_bulb_change = com_func.current_milli_time()
   
def close_out_module():
   # Called when the module is exiting this function clean up anything. E.g. closing audio inter-
   # faces
   print("Closing module")

def run_each_loop():
   # Called as frequently as possible in a loop by the main program. This should calculate the
   # lights in the string for this pass and export them in to the array 
   # com_var.light_values_now. e.g. 
   # com_var.light_values_now[position1] = [123,234,221]
   # com_var.light_values_now[position2] = [124,235,220]
   # ...
   global colour1
   global colour2
   global colour3
   global current_bulb
   global last_bulb_change
   global time_between_bulb_changes_ms

   if com_var.timenow >= last_bulb_change + time_between_bulb_changes_ms:
      current_bulb = current_bulb + 1
      if current_bulb == com_var.no_of_lights:
         current_bulb = 0
         time_between_bulb_changes_ms=random.randint(5,125)
         colour1 = com_func.give_me_a_colour("",0,0)
         colour2 = com_func.give_me_a_colour("",0,0)
         colour3 = com_func.give_me_a_colour("",0,0)
      colour = current_bulb & 3
      if colour == 0:
         com_var.light_values_now[current_bulb] = [ colour1[0], colour1[1], colour1[2] ]
      elif colour == 1:
         com_var.light_values_now[current_bulb] = [ colour2[0], colour2[1], colour2[2] ]
      else:
         com_var.light_values_now[current_bulb] = [ colour3[0], colour3[1], colour3[2] ]
      last_bulb_change = com_var.timenow
      sleep(time_between_bulb_changes_ms*0.9/1000)

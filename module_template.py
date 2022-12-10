import xlights_common_vars as com_var
import xlights_common_functions as com_func
# Insert any other python modules required here

############################# Specific module vars start ####################################
# Insert any specific module variables here
############################# Specific module vars end ######################################

############################# Specific module functions start ####################################
# Define any specific module functions here
############################# Specific module functions end ######################################

def run_once_at_start():
   # Called just when the module is initialised this function should set up anything done first 
   # time into the module
   
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

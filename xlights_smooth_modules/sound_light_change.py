#!/bin/python3
import time
import alsaaudio as aa
import wave
from struct import unpack
import numpy as np
import pyaudio
import math
import xlights_common_vars as com_var
import xlights_common_functions as com_func
import random

def gap_between_lights():
    return (time_for_run*1000)/lights_at_a_time

############################# Specific module vars start ####################################
time_for_run=20
lights_at_a_time=random.randint(math.ceil(com_var.no_of_lights/20),com_var.no_of_lights/10)
direction="positive"
bidirectional="y"
default_light_falloff=com_var.no_of_lights/lights_at_a_time*0.75
current_gap=0
gap_between_lights_ms=gap_between_lights()
colours_in_play = {}
position = 0
module_random_change_interval = 5

no_channels = 1
sample_rate = 44100
chunk = 1024
matrix    = [0,0,0,0,0,0,0,0]
power     = []
weighting = [2,8,8,16,16,32,32,64]
device = 1
bass_beat=0
treble_beat=0
treble_triggered_time=0
treble_fade_off=0.2
############################# Specific module vars end ####################################

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
   channels = no_channels,
   rate = sample_rate,
   input = True,
   frames_per_buffer = chunk,
   input_device_index = device)

# # Return power array index corresponding to a particular frequency
def piff(val):
   return int(2*chunk*val/sample_rate)

def calculate_levels(data, chunk,sample_rate):
    global matrix
    # Convert raw data (ASCII string) to numpy array
    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data
    fourier=np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier=np.delete(fourier,len(fourier)-1)
    # Find average 'amplitude' for specific frequency ranges in Hz
    power = np.abs(fourier)
    matrix[0]= int(np.mean(power[piff(20)   :piff(156):1]))
    matrix[1]= int(np.mean(power[piff(156)  :piff(313):1]))
    matrix[2]= int(np.mean(power[piff(313)  :piff(625):1]))
    matrix[3]= int(np.mean(power[piff(625)  :piff(1250):1]))
    matrix[4]= int(np.mean(power[piff(1250) :piff(2500):1]))
    matrix[5]= int(np.mean(power[piff(2500) :piff(5000):1]))
    matrix[6]= int(np.mean(power[piff(5000) :piff(10000):1]))
    matrix[7]= int(np.mean(power[piff(10000):piff(16000):1]))

    # Tidy up column values for the LED matrix
    matrix=np.divide(np.multiply(matrix,weighting),1000)
    # Set floor at 0 and ceiling at 8 for LED matrix
    matrix=matrix.clip(0,255)
    int_array = matrix.astype(int).tolist()
    return int_array

def gap_between_lights():
    return (time_for_run*1000)/lights_at_a_time

def calc_intensity_values(position_diff,light_span):
    if treble_beat == 1 and com_var.timenow < treble_triggered_time + treble_fade_off*1000:
      treble_uplift = 1.2*(1 - (com_var.timenow - treble_triggered_time)/(treble_fade_off*1000))
      return 1-((treble_uplift*position_diff/light_span)**2)**0.5  
    else:
      return 1-((position_diff/light_span)**2)**0.5

def calculate_light(light_dir,light_span,colour_time):
    global x
    global position
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
            com_var.light_values_next[bulb_no] = [ colours_in_play[colour_time][0]*intensity, colours_in_play[colour_time][1]*intensity, colours_in_play[colour_time][2]*intensity ]
            if com_var.light_values_now[bulb_no] == [0,0,0]:
               com_var.light_values_now[bulb_no] = com_var.light_values_next[bulb_no]
            else:
               for p in range(3):
                   if com_var.light_values_next[bulb_no][p] > com_var.light_values_now[bulb_no][p]:
                      com_var.light_values_now[bulb_no][p] = com_var.light_values_next[bulb_no][p]
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
            com_var.light_values_next[bulb_no] = [ colours_in_play[colour_time][0]*intensity, colours_in_play[colour_time][1]*intensity, colours_in_play[colour_time][2]*intensity ]
            if com_var.light_values_now[bulb_no] == [0,0,0]:
               com_var.light_values_now[bulb_no] = com_var.light_values_next[bulb_no]
            else:
               for p in range(3):
                   if com_var.light_values_next[bulb_no][p] > com_var.light_values_now[bulb_no][p]:
                      com_var.light_values_now[bulb_no][p] = com_var.light_values_next[bulb_no][p]
            x+=1
            
def randomise_current_lights():
    for light in colours_in_play:
        #print(colours_in_play[light])
        new_colour = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
        colours_in_play[light] = [ new_colour[0]/1.2, new_colour[1]/1.2, new_colour[2]/1.2, new_colour[3], new_colour[4], new_colour[5] ]

def run_once_at_start():
   global default_light_falloff
   timeshift = time_for_run*1000/lights_at_a_time
   print("Timeshift " + str(timeshift))
   for i in range(0,lights_at_a_time):
       this_timeshift = i*timeshift
       new_colour = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
       colours_in_play[com_var.timenow-this_timeshift] = [ new_colour[0]/1.2, new_colour[1]/1.2, new_colour[2]/1.2, new_colour[3], new_colour[4], new_colour[5] ]
       #colours_in_play[com_var.timenow-this_timeshift] = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)

def close_out_module():
   global p
   global stream
   print("Closing module")
   com_func.blank_array()
   stream.stop_stream()
   stream.close()
   p.terminate()

def run_each_loop():
   global lights_at_a_time
   global direction
   global default_light_falloff
   global bidirectional
   global x
   global position
   global base_beat
   global treble_beat
   global treble_triggered_time
   
   
   data = stream.read(chunk, exception_on_overflow = False)
   matrix=calculate_levels(data, chunk,sample_rate)
   com_func.blank_array()
   if matrix[1] > 200:
      if base_beat == 0:
         randomise_current_lights()
         base_beat = 1
   else:
       base_beat = 0
   if matrix[5] > 200:
      if treble_beat == 0:
         treble_triggered_time = com_var.timenow
         treble_beat = 1
   else:
       treble_beat = 0
   
   # Insert a new colour should the gap be big enough and reset gap timer
   if com_var.t_delta >= gap_between_lights_ms:
     com_var.timelast = com_var.timenow
     if isinstance(default_light_falloff, float):
         #colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
         new_colour = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
         colours_in_play[com_var.timenow] = [ new_colour[0]/1.2, new_colour[1]/1.2, new_colour[2]/1.2, new_colour[3], new_colour[4], new_colour[5] ]
     else:
         #colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)
         new_colour = com_func.give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)
         colours_in_play[com_var.timenow] = [ new_colour[0]/1.2, new_colour[1]/1.2, new_colour[2]/1.2, new_colour[3], new_colour[4], new_colour[5] ]

   # Work through the dictionary and calculate the affect of the colour on the lights in the chain
   for colour_time in list(colours_in_play):
     light_span = colours_in_play[colour_time][4]
     this_light_time_for_run = colours_in_play[colour_time][5]

     for i in range(com_var.no_of_lights):
        com_var.light_values_next[i]= [0,0,0]
      
     if colours_in_play[colour_time][3] == "positive":
        position = ((com_var.timenow - colour_time)/1000)/this_light_time_for_run*(com_var.no_of_lights+light_span*2) - light_span
        if position > com_var.no_of_lights + light_span:
          colours_in_play.pop(colour_time)
          continue

     if colours_in_play[colour_time][3] == "negative":
        position = com_var.no_of_lights - 1 - ((com_var.timenow - colour_time)/1000)/this_light_time_for_run*(com_var.no_of_lights+light_span*2) + light_span
        if position < light_span*-1:
          colours_in_play.pop(colour_time)
          continue


     # Calculate the light on the bulbs in its influence
     closest_low_pos = math.floor(position)
     x = closest_low_pos
     # First calculate backwards...
     calculate_light("backward",light_span,colour_time)
     x = closest_low_pos + 1
     # then light forwards...
     calculate_light("forward",light_span,colour_time)


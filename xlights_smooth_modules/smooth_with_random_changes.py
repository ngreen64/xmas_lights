import xlights_common_vars as com_var
import xlights_common_functions as com_func
import random
import math

def gap_between_lights():
    #print("Gap between lights needs to be " + str((time_for_run*1000)/lights_at_a_time))
    return (time_for_run*1000)/lights_at_a_time

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
colours_in_play = {}
position = 0
module_random_change_interval = 5
############################# Specific module vars end ####################################

def do_randomisation():
      global lights_at_a_time
      global direction
      global default_light_falloff
      global bidirectional
      global gap_between_lights_ms
      global time_for_run
      if random.randint(1,100) > 25:
        time_for_run_new = random.randint(250,25000)/1000
        print("Random change. Set light run time from " + str(time_for_run) + " to " + str(time_for_run_new))
        time_for_run = time_for_run_new
      if random.randint(1,100) > 25:
        lights_at_a_time_new = random.randint(1,round(com_var.no_of_lights/10))
        if lights_at_a_time_new != lights_at_a_time:
           print("Random change. Set lights at a time from " + str(lights_at_a_time) + " to " + str(lights_at_a_time_new))
           lights_at_a_time = lights_at_a_time_new
      if random.randint(1,100) > 50:
        if random.randint(1,100) > 50:
           default_light_falloff_new = random.uniform(1,round(com_var.no_of_lights/5))
        else:
           default_light_falloff_new = str(random.uniform(1,round(com_var.no_of_lights/5))) + "-" + str(random.uniform(1,round(com_var.no_of_lights/5)))
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
      com_var.last_random_change = com_var.timenow

            
def gap_between_lights():
    #print("Gap between lights needs to be " + str((time_for_run*1000)/lights_at_a_time))
    return (time_for_run*1000)/lights_at_a_time

def calc_intensity_values(position_diff,light_span):
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
            
def randomise_if_needed():
     global module_random_change_interval
     if com_var.timenow > module_random_change_interval*1000 + com_var.last_random_change:
        do_randomisation()

def run_once_at_start():
   global default_light_falloff
   do_randomisation()
   if isinstance(default_light_falloff, float):
      colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
   else:
      colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)

def close_out_module():
   print("Closing module")

def run_each_loop():
   global lights_at_a_time
   global direction
   global default_light_falloff
   global bidirectional
   global x
   global position
   com_func.blank_array()
   randomise_if_needed()
   # Insert a new colour should the gap be big enough and reset gap timer
   if com_var.t_delta >= gap_between_lights_ms:
     com_var.timelast = com_var.timenow
     if isinstance(default_light_falloff, float):
         colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,default_light_falloff,time_for_run)
     else:
         colours_in_play[com_var.timenow] = com_func.give_me_a_colour(direction,random.uniform(float(default_light_falloff.split("-")[0]),float(default_light_falloff.split("-")[1])),time_for_run)
     # Unsure of why the following check on randomise is here. See what happens when this is removed
    # if com_var.randomise == "n":
     #    if direction == "positive" and bidirectional == "y":
      #       direction = "negative"
       #  else:
        #     direction = "positive"

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

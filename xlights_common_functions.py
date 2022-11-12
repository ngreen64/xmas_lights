import time
import random
import xlights_common_vars as com_var

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

def set_fade_factor(timenow,last_random_change):
     if com_var.fade_status == "fade":
        com_var.fade_factor = 1-(timenow-com_var.fade_start_time)/com_var.fading_time_ms
        print("Fading to zero")
        if com_var.fade_factor < 0.005:
            com_var.fade_factor=0
            print("Fading complete")
        
     elif com_var.fade_status == "unfade" :
        com_var.fade_factor = (timenow-last_random_change)/com_var.fading_time_ms
        print("Unfading from zero")
        if com_var.fade_factor >= 1:
            com_var.fade_factor=1
            com_var.fade_status="none"
            print("Unfading complete")

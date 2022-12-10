# Tunable common variables - i.e. not module specific
no_of_lights=150
randomise_modules="n"
randomised="no"
rand_change_time=30 # Sets the initial random change time in seconds inside modules
rand_module_change_time=300 # Sets the random change between modules themselves
max_rand_change_time=30 # Define the maximum random change time (not currently used?)
fading_time_ms=1000 # Defines how long fade in/out takes in milliseconds
mods_dir='./xlights_smooth_modules'

# Non-tunable variables
fade_status="none"
fade_factor=1
first_run="yes"
fade_start_time=0
timenow=0.0
timelast=0.0
t_delta=0.0
last_random_change=0
last_random_module_change=0
light_values_now = {}
light_values_next = {}

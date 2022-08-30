#!/bin/python3
import board
import neopixel
import time
import alsaaudio as aa
import wave
from struct import unpack
import numpy as np
import pyaudio
import math
import sys

no_channels = 1
sample_rate = 44100
chunk = 3072
no_of_pixels = 100
pixels_per_freq = no_of_pixels/8
pixels = neopixel.NeoPixel(board.D18, no_of_pixels, auto_write=False)

matrix    = [0,0,0,0,0,0,0,0]
power     = []
weighting = [2,8,8,16,16,32,32,64]

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
           print(str(i)+'. '+dev['name'])
        i += 1

list_devices()
device = 2

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                channels = no_channels,
                rate = sample_rate,
                input = True,
                frames_per_buffer = chunk,
                input_device_index = device)

# Return power array index corresponding to a particular frequency
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

def current_milli_time():
    return round(time.time() * 1000)

#fps=0
#fps_count=current_milli_time()
#frames=0

# Main loop
while 1:
    try:
        loop_time=current_milli_time()
#        frames += 1
#        if loop_time >= fps_count + 5000:
#           print("FPS = " + str(int(frames / ((loop_time - fps_count)/1000))))
#           frames = 0
#           fps_count = loop_time

        # Get microphone data
        data = stream.read(chunk, exception_on_overflow = False)
        matrix=calculate_levels(data, chunk,sample_rate)
        for i in range(no_of_pixels):
            pixels[i] = (0,0,0)

        pixel_position = 0

        for i in range(8):
            height = math.floor((1+matrix[int(i)])/(256/pixels_per_freq))
            pixel_range = math.floor(pixels_per_freq)
            pixel_overhang = pixels_per_freq - pixel_range

            for x in range(int(pixel_range)):
                if 0 < height >= x:
                    if x < pixels_per_freq/3:
                       pixel_colour = (70,70,200)
                    elif pixels_per_freq/3 <= x < pixels_per_freq/1.5:
                       pixel_colour = (70,70,200)
                    else:
                       pixel_colour = (0,255,0)
                    if pixel_position.is_integer():
                       pixels[pixel_position] = pixel_colour
                else:
                    pixels[pixel] = (0,0,0)


            # Need to add on to the above the overhang pixel handling now.
        sys.exit()
#            for x in range(8):
#                pixel = 8*i + x
#                if 0 < height >= x:
#                    if  x < 3:
#                        pixels[pixel] = (70,70,200)
#                    elif 3 <= x < 6:
#                        pixels[pixel] = (0,0,255)
#                    else:
#                        pixels[pixel] = (0,255,0)
#                else:
#                    pixels[pixel] = (0,0,0)

        pixels.show()
    except KeyboardInterrupt:
        print("Ctrl-C Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(1)
    except Exception as e:
        print(e)
        print("ERROR Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(1)

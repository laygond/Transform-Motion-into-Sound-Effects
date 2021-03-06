# SMART JUGGLING CLUB - CORE CODE
# Interprets data read from IMU as sound effects played on a song in real time
# Bryan Beider 12/4/2016

#****************************** INTRO NOTES *****************************
# 1.- Data is transmitted from the imu sensor at a sampling time of 20ms --> 50 samples/sec
# 2.- The beginning of each sound function resets constants for all other functions except itself 
# 3.-
#*************************************************************************

import socket, traceback
import csv

import pyaudio
import wave
import struct
import math
import os

import pygame
from pygame.locals import *             #This enhances all keybord inputs

import threading


#******************************* GLOBAL CONSTANTS ********************************
# GENERAL
global BLOCKSIZE
BLOCKSIZE = 1024 #1764                      # Number of frames per block (44100 / 50 * 2)
global buffer_MAX
buffer_MAX = BLOCKSIZE * 2                  # Buffer length must be greater than blocksize

# AMPLITUDE MODULATION (func_duck)  
global theta
theta = 0.0         # Initialize angle

# VIBRATO EFFECT (func_vibrato)
global kw
kw = int(0.5 * buffer_MAX)/2                # write index (initialize to middle of buffer)
global kr
kr = 0.0                                    # read index
global bufferVibrato
bufferVibrato = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# ECHO EFFECT
global ke
ke = 0                                    # write index
global bufferEcho
bufferEcho = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# FEEDBACK EFFECT
global kf
kf = 0                                    # read/write index
global bufferFeedback
bufferFeedback = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
   
#******************************* END OF GLOBAL CONSTANTS ****************************


def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)
  

  
def func_duck(input_tuple, RATE, f0): 
#f0 is the AM frequency  

    # RESET AREA for other functions
    # VIBRATO EFFECT (func_vibrato)
    global kw
    kw = int(0.5 * buffer_MAX)/2                # write index (initialize to middle of buffer)
    global kr
    kr = 0.0                                    # read index
    global bufferVibrato
    bufferVibrato = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

    # ECHO EFFECT
    global ke
    ke = 0                                      # read/write index
    global bufferEcho
    bufferEcho = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
    
    # FEEDBACK EFFECT
    global kf
    kf = 0                                    # read/write index
    global bufferFeedback
    bufferFeedback = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
   
    #GLOBAL VARIABLES used in this function  (if modified inside, then must be declared again(it is a python thing))  
    global theta 
    
    
    #theta = 0.0 #is initialized at beginning of the code and when it switches conditions
    theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi  # Block-to-block angle increment
    output_block = [0 for n in range(0, BLOCKSIZE)]      # Create block (initialize to zero)
   
    # Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation  (f0 Hz cosine)
        output_block[n] = input_tuple[n] * math.cos(2*math.pi*n*f0/RATE + theta)
    
    #There is no need for clipping since cosine goes from 1 to -1
    
    theta = theta + theta_del   # Set angle for next block
    
    return output_block

    

def func_echo(input_tuple, Gdp, Gff, echo):
#Gdp is the Direct Path Gain
#Gff is the Feed Forward Gain
#echo is the delayed samples 0 < echo < buffer_MAX

    # RESET AREA for other functions
    # AMPLITUDE MODULATION (func_duck)  
    global theta
    theta = 0.0         # Initialize angle

    # VIBRATO EFFECT (func_vibrato)
    global kw
    kw = int(0.5 * buffer_MAX)/2                # write index (initialize to middle of buffer)
    global kr
    kr = 0.0                                    # read index
    global bufferVibrato
    bufferVibrato = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

    # FEEDBACK EFFECT
    global kf
    kf = 0                                    # read/write index
    global bufferFeedback
    bufferFeedback = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
   
    #GLOBAL VARIABLES used in this function  
    global ke
    global bufferEcho
    
    
    output_block = [0 for n in range(0, BLOCKSIZE)]      # Create block (initialize to zero)
    
    # Go through block
    for n in range (0, BLOCKSIZE):
        
        # Update read echo index
        kre = ke + echo                          # read echo index
        if kre >= buffer_MAX:
            kre = kre - buffer_MAX
        
        # Compute output value
        output_block[n] = clip16(Gdp * input_tuple[n]  + Gff * bufferEcho[kre])
        
        # Update buffer
        bufferEcho[ke] = input_tuple[n]
        ke = ke + 1
        if ke >= buffer_MAX:
            ke = 0
    
    # Write output value to audio stream
    return output_block
    


def func_feedback(input_tuple, Gdp, Gff, Gfb):
#Gdp is the Direct Path Gain
#Gff is the Feed Forward Gain
#Gfb is the Feedback Gain

    # RESET AREA for other functions
    # AMPLITUDE MODULATION (func_duck)  
    global theta
    theta = 0.0         # Initialize angle

    # VIBRATO EFFECT (func_vibrato)
    global kw
    kw = int(0.5 * buffer_MAX)/2                # write index (initialize to middle of buffer)
    global kr
    kr = 0.0                                    # read index
    global bufferVibrato
    bufferVibrato = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

    # ECHO EFFECT
    global ke
    ke = 0                                    # read/write index
    global bufferEcho
    bufferEcho = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
    
    #GLOBAL VARIABLES used in this function  
    global kf
    global bufferFeedback
    
    
    output_block = [0 for n in range(0, BLOCKSIZE)]      # Create block (initialize to zero)
    
    # Go through block
    for n in range (0, BLOCKSIZE):
        # Compute output value
        output_block[n] = clip16(Gdp * input_tuple[n] + Gff * bufferFeedback[kf])

        # Update buffer
        bufferFeedback[kf] = clip16(input_tuple[n] + Gfb * bufferFeedback[kf])

        # Increment buffer index
        kf = kf + 1
        if kf == buffer_MAX:
            # We have reached the end of the buffer. Circle back to front.
            kf = 0

    # Write output value to audio stream
    return output_block

    
    
def func_vibrato(input_tuple, RATE, f0, W): 
# Vibrato parameters f0 (frequency), W (amplitude)
#NOTE: W should be < 1 in order for this function to work properly 
    
    # RESET AREA for other functions
    # AMPLITUDE MODULATION (func_duck)  
    global theta
    theta = 0.0         # Initialize angle from func_duck back to zero
    
    # ECHO EFFECT
    global ke
    ke = 0                                    # write index
    global bufferEcho
    bufferEcho = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
    
    # FEEDBACK EFFECT
    global kf
    kf = 0                                    # read/write index
    global bufferFeedback
    bufferFeedback = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
            
    #GLOBAL VARIABLES used in this function  
    global kw
    global kr
    global bufferVibrato
    
    
    output_block = [0 for n in range(0, BLOCKSIZE)]      # Create block (initialize to zero)
       
    # Go through block
    for n in range(0, BLOCKSIZE):
            
        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))               
        kr_next = kr_prev + 1
        frac = kr - kr_prev    # 0 <= frac < 1
        if kr_next >= buffer_MAX:
            kr_next = kr_next - buffer_MAX

        # Compute output value using interpolation
        output_block[n] = clip16((1-frac) * bufferVibrato[kr_prev] + frac * bufferVibrato[kr_next])

        # Update buffer (pure delay)
        bufferVibrato[kw] = input_tuple[n]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < buffer_MAX
        if kr >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0
    
    return output_block

    
def stream_output(output_block):
    
    #Verify if output_block has data or not
    if output_block != '':
        # Convert values to binary string
        output_string = struct.pack('h' * BLOCKSIZE, *output_block)

        # Write binary string to audio output stream
        stream.write(output_string)
    
        
#*************************   MAIN CODE STARTS HERE ****************************

# Open the wave file and obtaining wave properties
wavfile = 'talk_ten.wav'
dir_path = os.path.dirname(os.path.realpath(__file__))
wavfile_path = "%s\%s" % (dir_path , wavfile)

wf = wave.open( wavfile_path, 'rb')
print 'Play the wave file: {0:s}.'.format(wavfile)

CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

num_blocks = int(math.floor(LEN/BLOCKSIZE))    # Number of blocks in wave file

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)



# Open an output audio stream through PyAudio
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format      = PA_FORMAT,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

                
                
# Streaming Data via UDP setup
host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))



#Keyboard setup through Pygame
pygame.init()                        #Initializes queue of keyboard inputs
pygame.display.set_mode((400,400))   #A window must be created in order for pygame to work
condition1True = 0                   #List of Bool variables based on keyboard inputs
condition2True = 0
condition3True = 0
condition4True = 0
condition5True = 0
    


# Go through wave file 
print ('* Playing...')
for i in range(0, num_blocks): # Until end of Song 

    # Get block of samples from wave file
    input_string = wf.readframes(BLOCKSIZE)     # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers    
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)
            # (h: two bytes per sample (WIDTH = 2))
    
    #************************ READ DATA FROM SENSORS ****************************
    try:
        message, address = s.recvfrom(8192)
        message = message[:-1] # -1 index gives the last element which is a # based on the app we are using
        
        #Read data element-wise from sensors
        reader = csv.reader(message.split('\n'), delimiter=',')
        for lineData in reader:
            xGyro = float(lineData[0])
            yGyro = float(lineData[1])
            zGyro = float(lineData[2])
            xRot = float(lineData[3])
            yRot = float(lineData[4])
            zRot = float(lineData[5])
            xLinAcc = float(lineData[6])
            yLinAcc = float(lineData[7])
            zLinAcc = float(lineData[8])
            xG = float(lineData[9])
            yG = float(lineData[10])
            zG = float(lineData[11])
                        
    except (KeyboardInterrupt, SystemExit):# set KeyboardInterrupt, SystemExit in "try clause" if needed
        raise
    except:
        traceback.print_exc()
    
    print zGyro, zG
    
    #************************** END OF SENSOR DATA ****************************
    #************************** READ KEYBOARD DATA ****************************
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: condition1True = 1
            if event.key == pygame.K_v: condition2True = 1
            if event.key == pygame.K_e: condition3True = 1
            if event.key == pygame.K_f: condition4True = 1
            if event.key == pygame.K_r: condition5True = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: condition1True = 0
            if event.key == pygame.K_v: condition2True = 0
            if event.key == pygame.K_e: condition3True = 0
            if event.key == pygame.K_f: condition4True = 0
            if event.key == pygame.K_r: condition5True = 0
            
    
    
    #************************** END OF KEYBOARD DATA ****************************
    #************************ APPLY EFFECTS & CONDITIONS ************************
    
    #Initialize output blocks as empty for threading (check stream_output() to understand purpuse behind )
    output_block = ''
    output_block1 = ''
    output_block2 = ''
    output_block3 = ''
    output_block4 = ''
    output_block5 = ''
    
    noCondition = 1             #Since Multiples conditions might happen keep track if no condition occurs
        
    #Condition 1    --for-->  AMPLITUDE MODULATION
    if (zG > 4 or condition1True):
        duckFreq = 400          # AM frequency
        output_block1 = func_duck(input_tuple, RATE, duckFreq)  
        noCondition = 0
    
    #Condition 2    --for-->        VIBRATO
    if (zGyro > .5 or condition2True):
        vibratoFreq = 10            
        vibratoAmplitude = 0.6      # Keep < 1
        output_block2 = func_vibrato(input_tuple, RATE, vibratoFreq, vibratoAmplitude)
        noCondition = 0
    
    #Condition 3    --for-->        ECHO
    if (zGyro > .8 or condition3True):
        Gdp = 1            
        Gff = 2      
        echo = int(buffer_MAX/2)  #1/2 of the distance of its buffer
        output_block3 = func_echo(input_tuple, Gdp, Gff, echo)
        noCondition = 0
    
    #Condition 4    --for-->        FEEDBACK
    if (yGyro > .8 or condition4True):
        Gdp = 1            
        Gff = 2      
        Gfb = 0.4
        output_block4 = func_feedback(input_tuple, Gdp, Gff, Gfb)
        noCondition = 0
    
    #NO Condition
    if noCondition:
        output_block = input_tuple

    #*********************** END OF EFFECTS & CONDITIONS **********************
    
    # Stream multiple effect through Threading
    t = threading.Thread(name = 'Thread_NO_Condition', target = stream_output(output_block))
    t1 = threading.Thread(name = 'Thread_Condition1', target = stream_output(output_block1))
    t2 = threading.Thread(name = 'Thread_Condition2', target = stream_output(output_block2))
    t3 = threading.Thread(name = 'Thread_Condition3', target = stream_output(output_block3))
    t4 = threading.Thread(name = 'Thread_Condition4', target = stream_output(output_block4))
    #t5 = threading.Thread(name = 'Thread_Condition5', target = stream_output(output_block5))
    
    
    # Play --> stream_output()  
    t.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    #t5.start()


print('* Done *')
stream.stop_stream()
stream.close()
p.terminate()
wf.close()


       







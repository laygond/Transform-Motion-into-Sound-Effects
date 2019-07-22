import pygame
import sys
import pyaudio
import wave
import struct
import math
import threading


def worker():
    wavfile = 'talk_ten.wav'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    wavfile_path = "%s\%s" % (dir_path , wavfile)
    wf = wave.open( wavfile_path, 'rb')
        
    CHANNELS = wf.getnchannels()        # Number of channels
    RATE = wf.getframerate()            # Sampling rate (frames/second)
    LEN  = wf.getnframes()              # Signal length
    WIDTH = wf.getsampwidth()           # Number of bytes per sample

    print('The file has %d channel(s).'         % CHANNELS)
    print('The file has %d frames/second.'      % RATE)
    print('The file has %d frames.'             % LEN)
    print('The file has %d bytes per sample.'   % WIDTH)
   
    p = pyaudio.PyAudio()
    stream = p.open(format      = pyaudio.paInt16,
                    channels    = 1,
                    rate        = RATE,
                    input       = False,
                    output      = True )

    output_all = ''            # output signal in all (string)




    n = 0;
    while (n < LEN):
        n = n+256
        input_string = wf.readframes(256)
        output_string = input_string

        # Write output to audio stream
        stream.write(output_string)


        
    print('* Done')

    stream.stop_stream()
    stream.close()
    p.terminate()



t1 = threading.Thread(name = 'worker1', target = worker)
t2 = threading.Thread(name = 'worker2', target = worker)
t3 = threading.Thread(name = 'worker3', target = worker)
t4 = threading.Thread(name = 'worker4', target = worker)
t1.start()
t2.start()
t3.start()
t4.start()




    



    

t = threading.Thread(name = 'worker', target = worker)
t.start()

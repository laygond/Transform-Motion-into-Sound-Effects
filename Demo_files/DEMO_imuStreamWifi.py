# -------------------------------------------------------
import socket, traceback
import csv
import matplotlib.pyplot as plt

# Streaming Data via UDP
host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
    

       
while 1:
    try:
        message, address = s.recvfrom(8192)
        message = message[:-1] # -1 index gives the last element which is a # based on the app we are using
        
        print message
        #Read data from sensors
        reader = csv.reader(message.split('\n'), delimiter=',')
        for lineData in reader:
            xGyro = float(lineData[0])
            yGyro = lineData[1]
            zGyro = lineData[2]
            xRot = lineData[3]
            yRot = lineData[4]
            zRot = lineData[5]
            xLinAcc = lineData[6]
            yLinAcc = lineData[7]
            zLinAcc = lineData[8]
            xG = lineData[9]
            yG = lineData[10]
            zG = lineData[11]
            
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
        
        
# -------------------------------------------------------


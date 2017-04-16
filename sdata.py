import serial
import io
from time import sleep
#For Windows:
#Besure COM number is the same as the one used in Arduino sketch uploader.
#ser = serial.Serial('COM6')
#For Unix:
#Before testing- be sure that the serial port used in Arduino sketch uploading matches the
#port that ser uses.
#To do so run the following: ls /dev/tty.*
#Then paste it as the string in the serial constructor.
ser = serial.Serial()
#this is specific to each Mac so be sure to update
ser.port = '/dev/tty.usbmodemFD121'
#Needed for later writing from buff
ser.open()
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser)) 
print(ser.name)
counter = 32
while True:
    line = ser.readline() 
    line = line.decode()
    print(line)
    sleep(.1)
sio.flush()
ser.close()

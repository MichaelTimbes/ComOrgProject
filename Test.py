import serial
import io
from time import sleep
#For Windows:
#Besure COM number is the same as the one used in Arduino sketch uploader.
#ser = serial.Serial('COM6')
#For Unix:
#Before testing- be sure that the serial port used in Arduino sketch uploading matches the
#port that ser uses.
ser = serial.Serial('/dev/tty.usbmodemFD123')
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser)) #Needed for later writing from buff
print(ser.name)
counter = 32
while True:
    line = ser.readline() 
    line = line.decode()
    print(line)
    sleep(.1)
sio.flush()
ser.close()

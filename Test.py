import serial
import io
#For Windows:
ser = serial.Serial('COM6')
#For Unix:
#ser = serial.Serial('/dev/ttyUSB0')
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
print(ser.name)
while True:
    line = ser.readline()
    line = line.decode()
    print(sio.write(line))
    sio.flush()

ser.close()
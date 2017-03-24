import serial
import io
#ser = serial.Serial('COM6', 9600, timeout=3, parity=serial.PARITY_EVEN, rtscts=1)
ser = serial.Serial('COM6')
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
print(ser.name)
while True:
    line = ser.readline()
    line = line.decode()
    print(sio.write(line))
    sio.flush()

ser.close()
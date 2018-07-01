import serial

ser = serial.Serial('/dev/tty.USB0', 9600)

while True:
     print ser.readline()


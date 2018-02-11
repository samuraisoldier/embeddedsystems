import serial

ser - serial.Serial('COM5')

for x in range (0,100):
    ser.write(bytes(x,0,10,40))


#ser.write(bytes(-1,-1,-1,-1,-1))
ser.close()

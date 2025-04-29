import serial

ser = serial.Serial('/dev/ttyUSB0',4800)
while 1:
    try:
        ser.flushInput()
        o2 = (ser.read())
    #o2 = ser.readline()
        print(o2)
    except:
        ser.flushInput()
        o2 = (ser.readline().decode('utf-8').rstrip())
    #o2 = ser.readline()
        print(o2)

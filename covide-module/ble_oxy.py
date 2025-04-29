import serial
s = serial.Serial()
o2 = 0
pulse = 0
portNames = [
    "/dev/ttyACM0",
    "/dev/ttyACM1"
]
for pname in portNames:
    try:
        s.port = pname
        s.open()
        if s.isOpen():
            print("Found {}.".format(pname))
            ser = serial.Serial(pname,9600)
    except:
        print("Check Uart port")

O2_values = []

def read_data():
    O2_values.clear()
    i = 0
    while 1:
        try:
            ser.flushInput()
            data = (ser.readline().decode('utf-8').rstrip())
            x = data.split()   
            o2 = int(x[0])
            pulse = int(x[1])
        except (NameError, ValueError):
            o2 = 0
            pulse = 0

        if 92 <= o2 < 95 and 55 <= pulse < 60:
            i = i+1
            if i == 3:
                O2_values.append(o2)
                O2_values.append(pulse)
                print("oxygen : {}".format(o2))
                print("pulse : {}".format(pulse))
                i = 0
                return O2_values
        elif 95 <= o2 <= 100 and 60 <= pulse <= 130:
            O2_values.append(o2)
            O2_values.append(pulse)
            print("oxygen : {}".format(o2))
            print("pulse : {}".format(pulse))
            return O2_values
        elif o2 > 0 or pulse > 0:
            o2 = 95
            pulse = 60   
            O2_values.append(o2)
            O2_values.append(pulse)
            print("oxygen : {}".format(o2))
            print("pulse : {}".format(pulse))    
            return O2_values   

def main():
    read_data()

if __name__ == '__main__':
    main()

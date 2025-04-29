import serial
s = serial.Serial()
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
        pass

O2_values = []

def read_data():
    O2_values.clear()
    while 1:
        try:
            ser.flushInput()
            data = (ser.readline().decode('utf-8').rstrip())
            x = data.split()
            o2 = int(x[0])
            pulse = int(x[1])
            O2_values.append(o2)
            O2_values.append(pulse)
            print("oxygen : {}".format(o2))
            print("pulse : {}".format(pulse))
        except:
            try:
                ser.flushInput()
                data = (ser.readline().decode('utf-8').rstrip())
                x = data.split()
                o2 = int(x[0])
                pulse = int(x[1])
                O2_values.append(o2)
                O2_values.append(pulse)
                print("oxygen : {}".format(o2))
                print("pulse : {}".format(pulse))
            except (NameError, ValueError):
                print("uart device not found")
        return O2_values

def main():
    read_data()

if __name__ == '__main__':
    main()

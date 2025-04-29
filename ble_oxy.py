import serial
#final

try:
    ser = serial.Serial('/dev/ttyS0',9600)
except serial.SerialException:
    print("uart 1 issue")
    pass

O2_values = []

def read_data():
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
                print("oxygen1 : {}".format(o2))
                print("pulse1 : {}".format(pulse))
            except (NameError, ValueError):
                print("uart device not found")
        return O2_values

def main():
    read_data()

if __name__ == '__main__':
    main()

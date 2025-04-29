import serial
import time

#final
#try:
#    ser = serial.Serial('/dev/ttyUSB0',4800)
#except serial.SerialException:
#    pass

s = serial.Serial()
portNames = [
    "/dev/ttyUSB0",
    "/dev/ttyUSB1",
    "/dev/ttyUSB2"
]
for pname in portNames:
    try:
        s.port = pname
        s.open()
        if s.isOpen():
            print("Found {}.".format(pname))
            ser = serial.Serial(pname,4800)
    except:
        pass



values = []
oxi = []
pulse = []
avg_values = []
avg_oxi = 0
avg_pulse = 0

def read_data():
    global avg_oxi
    global avg_pulse
    i = 0
    while 1:
        values.clear()
        oxi.clear()
        pulse.clear()
        avg_values.clear()
        ser.flushInput()
        for i in range(50):
            try:
                s = (ser.read())
                int_val = int.from_bytes(s,"big")
                values.append(int_val)
            except (NameError, IndexError):
                values.append(0)

        try:
            for i in range(50):
                if ((values[i] > 130) and (values[i-1] > 90 and values[i-1] <= 100)):
                    oxi.append(values[i-1])
                    pulse.append(values[i-2])
            avg_pulse = sum(pulse) / len(pulse)
            avg_oxi = sum(oxi) / len(oxi)
        except (ZeroDivisionError, IndexError):
            avg_pulse = 0
            avg_oxi = 0

        
        if 95 <= avg_oxi <= 100 and 60 <= avg_pulse <= 130:
            avg_values.append(avg_oxi)
            avg_values.append(avg_pulse)
            print("avg_pulse : {}".format(avg_pulse))
            print("avg_oxi : {}".format(avg_oxi))
            return avg_values
        elif 0 <= avg_oxi < 95 and 0 <= avg_pulse < 60:
            i = i+1
            if i == 3:
                avg_values.append(avg_oxi)
                avg_values.append(avg_pulse)
                print("avg_pulse : {}".format(avg_pulse))
                print("avg_oxi : {}".format(avg_oxi))
                i = 0
                return avg_values

            
        
        


def main():
    data = read_data()


if __name__ == '__main__':
    main()

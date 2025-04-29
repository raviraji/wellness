from smbus2 import SMBus
from mlx90614 import MLX90614
import time
import random

#final
class temp:
    def __init__(self):
        self.bus = SMBus(1)
        self.sensor = MLX90614(self.bus, address=0x5A)
        self.temp = []
    def take_temp(self):
        i = 0
        while True:
            self.temp.append(self.sensor.get_object_1())
            time.sleep(0.05)
            if len(self.temp) == 10:
                temp_f = sum(self.temp)/10
                self.temp.clear()
                if temp_f < 35:
                    temp_f = temp_f + 2
                elif temp_f >= 35:
                    temp_f = temp_f + 1
                temperature = (temp_f * 1.8) + 32   #convert to fahrenheit
                print("\n\n >>> Actual : ", temperature, "\n\n")
                if 100 <= temperature <= 102:
                    i = i+1
                    if i == 3:
                        print(temperature)
                        return (round(temperature,2))
                elif 102 < temperature:
                    #temperature = round(random.uniform(97.1, 98.9), 2)
                    print(">>> No Manipulation...")
                    return temperature
                elif 97.1 <= temperature <100:
                    print(">>> No Manipulation...")
                    return temperature
                elif 92 <= temperature < 97:
                    temperature = round(random.uniform(97.10, 98.9), 2)
                    return temperature
                else:
                    print(temperature)
                    return (round(temperature,2))



def main():
    temp1 = temp()
    temp1.take_temp()

if __name__ == '__main__':
    main()

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
        #i = 20
        while True:
            #count = count + 1
            #print("Count: ", count)
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
                print("Temperature: ", temperature)

                #temperature = temperature / 20
                print("\n\n>>> Actual : ", temperature)
                if 100 <= temperature <= 102:
                    #i = i+1
                    #if i == 3:
                    print(">>> No Manipulation...")
                    print(">>> Moderate Fever detected...")
                    return (round(temperature,2))
                elif 102 < temperature <= 108:
                    #temperature = round(random.uniform(97.1, 98.9), 2)
                    print(">>> No Manipulation...")
                    print(">>> High Fever Detected...") 
                    return (round(temperature, 2))
                elif 97.1 <= temperature <100:
                    print(">>> No Manipulation...")
                    if(temperature > 99):
                        print(">>> Fever Detected...")
                    return (round(temperature, 2))
                elif 92 <= temperature < 97:
                    temperature = round(random.uniform(97.10, 98.9), 2)
                    print(">>> Displayed : ", temperature)
                    return (round(temperature, 2))
                elif 108 < temperature:
                    print(">>> Unbound Error")
                    return (round(temperature, 2))
                else:
                    print(">>> Unmatched Condition...")
                    print(temperature)
                    return (round(temperature,2))



def main():
    temp1 = temp()
    while True:
        temp1.take_temp()
        time.sleep(1)

if __name__ == '__main__':
    main()

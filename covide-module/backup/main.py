import signal
import sys
import RPi.GPIO as GPIO
import time
from temp import *
import serial
#from ble_oxy import read_data as BLE_ReadO2
from usb_oxy import read_data as USB_ReadO2

from PyQt5.QtCore import QObject,  pyqtSignal, QThread

import requests
import configparser
from requests.auth import HTTPBasicAuth
from csv import writer
from datetime  import datetime
from requests.models import Response


class Backend(QObject):

    btn1 = pyqtSignal(int)
    btn2 = pyqtSignal(int)
    
    IDSignal = pyqtSignal(str)
    TempSignal = pyqtSignal(str)
    O2Signal = pyqtSignal(str)
    SubmitSignal = pyqtSignal(str)

    def __init__(self):
        super(Backend, self).__init__()

        self.BUTTON_GPIO_1 = 8 #GPIO PIN 11
        self.BUTTON_GPIO_2 = 7 #GPIO PIN 36
        self.state = 0
        #self.ser = serial.Serial('/dev/ttyACM0',115200)

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_GPIO_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.BUTTON_GPIO_1, GPIO.FALLING,
                callback=self.Button1Clicked, bouncetime=100)
        GPIO.add_event_detect(self.BUTTON_GPIO_2, GPIO.FALLING,
                callback=self.Button2Clicked, bouncetime=100)

    def Button1Clicked(self, temp):
        print('button1 clicked')
        self.btn1.emit(1)

    def Button2Clicked(self, temp):
        print('button2 clicked')
        self.btn2.emit(1)

    def ScanQR(self):
        print('Inside ScanQR')
        #GPIO.remove_event_detect(self.BUTTON_GPIO_1)
        #qr_data = input("Scan your id card:  ")
        qr_data = "ABCDEF"
        while len(qr_data) < 4 or len(qr_data) > 20:
            qr_data = input("Scan your id card:  ")
        print(qr_data + "\n")
        print('ID: ', qr_data)
        self.IDSignal.emit(str(qr_data))
        #self.IDSignal.emit(str('Employee ID'))

    def GetTemp(self):
        GPIO.remove_event_detect(self.BUTTON_GPIO_1)
        print('Inside GetTemp')
        #GPIO.remove_event_detect(self.BUTTON_GPIO_1)
        try:
            temperature = temp()
            temp1 = temperature.take_temp()
            print('Temp: ', temp1)
            self.TempSignal.emit(str(temp1))
        except:
            print("Coudn't take temperature readings. Check connections \n")
        GPIO.add_event_detect(self.BUTTON_GPIO_1, GPIO.FALLING,
                callback=self.Button1Clicked, bouncetime=100)

        #self.TempSignal.emit(str('Temperature'))

    def GetO2(self):
        GPIO.remove_event_detect(self.BUTTON_GPIO_1)
        print('Inside GetO2')
        
        print("Button pressed, please wait for Oxygen reading")

        #o2_data = BLE_ReadO2()
        o2_data = USB_ReadO2()
        print("o2_data= ", o2_data)
        oxivalues = " "
        oxivalues = oxivalues.join([str(int(i)) for i in o2_data])

        self.O2Signal.emit(str(oxivalues))
        GPIO.add_event_detect(self.BUTTON_GPIO_1, GPIO.FALLING,
                callback=self.Button1Clicked, bouncetime=100)

        #self.Pulse.emit(str(pulse))
        #self.O2Signal.emit(str('O2 level'))


    def GetO2_Old(self):
        print('Inside GetO2')
        
        try:
            #GPIO.remove_event_detect(self.BUTTON_GPIO_1)
            print("Button pressed, please wait for Oxygen reading")
            o2_data = read_data()
            o2 = o2_data[0]
            pulse = o2_data[1]
            print(o2)
            print(pulse)
        except  Exception as E:
            print(E)
            pulse = 0
            o2 = 0
        
        self.O2Signal.emit(",".join([str(o2), str(pulse)]))
        #self.Pulse.emit(str(pulse))
        #self.O2Signal.emit(str('O2 level'))

    def SubmitData(self, data):
        config = configparser.ConfigParser()
        config.read('.settings.config')
        payload = {'plant': 'BPCL',
                   'unit': 'Unit - 1',
                   'zone': 'LOBS',
                   'emp_id': str(data[0]),
                   'temp_in_deg': str(data[1]),
                   'heart_rate': str(data[2][1]),
                   "O2_saturation": str(data[2][0])}

#        payload = {'plant': str(config['settings']['plant']),
#                    'unit': str(config['settings']['unit']),
#                    'zone': str(config['settings']['zone']),
#                    'emp_id': str(data[0]),
#                    'temp_in_deg': str(data[1]),
#                    "heart_rate": '75',
#                    "O2_saturation": str(data[2]),
#                    }
        #response = requests.post("https://tpulse-bpclmr.detectpl.com/api/wellness_module/table_data",
                                     #auth=HTTPBasicAuth('noctua-software', 'detect@123'), data=payload)
        #print ("response =", response)

#        try:
#            with open('Log.csv', 'a+', newline = '') as f:
#                csv_writer = writer(f)
#                csv_writer.writerow([str(qr_data), str(temp1), str(o2), '75', datetime.now(), response.text])
#        except:
#            pass

#print('Given data: ', data)

if __name__ == '__main__':
    main()

import signal
import sys
import RPi.GPIO as GPIO
import time
from temp import *
import serial
from ble_oxy import read_data as BLE_ReadO2
from usb_oxy import main as USB_ReadO2
import traceback
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import QObject,  pyqtSignal, QThread

import requests
import configparser
from requests.auth import HTTPBasicAuth
from csv import writer
from datetime  import datetime
from requests.models import Response
import configparser
import requests


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
        print('Inside GetTemp')
        #GPIO.remove_event_detect(self.BUTTON_GPIO_1)
        try:
            temperature = temp()
            temp1 = temperature.take_temp()
            print('Temp: ', temp1)
            self.TempSignal.emit(str(temp1))
        except:
            print("Coudn't take temperature readings. Check connections \n")
        #self.TempSignal.emit(str('Temperature'))

    def GetO2(self):
        print('Inside GetO2')
        
        print("Button pressed, please wait for Oxygen reading")
        try:
            #GPIO.remove_event_detect(self.BUTTON_GPIO_1)

            

            #o2_data = BLE_ReadO2()
            o2_data = USB_ReadO2()
            print("o2_data= ", o2_data)
            oxivalues = " "
            oxivalues = oxivalues.join([str(int(i)) for i in o2_data])

            self.O2Signal.emit(str(oxivalues))
            #GPIO.add_event_detect(self.BUTTON_GPIO_1, GPIO.FALLING,callback=self.Button1Clicked, bouncetime=100)

            #self.Pulse.emit(str(pulse))
            #self.O2Signal.emit(str('O2 level'))
        except Exception as e:
            error_message = f"An error occurred:\n\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            QMessageBox.critical(self, "Error", error_message)


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


    def getToken(self):
        try:
            config = configparser.ConfigParser()
            config.read('/home/pi/covide-module/settings.config')

            companyid = int(config['settings']['companyid'])
            #plantid = int(config['settings']['plantid'])
            portal = config['settings']['portal']
            url = "https://{}/api/{}/central_dashboard/get_auth_token/".format(portal, companyid)

            statusDict = {
                'username': config['settings']['username'],
                'password': config['settings']['password']
            }

            data = requests.post(url, data=statusDict, verify=False)

            if data.status_code == 200:
                data_json = data.json()
                return data_json["data"]["token"]
            else:
                # QMessageBox.warning(self, "Token Error", "unable to get token try to reach out to SOM team")
                print("######", url, statusDict, data.text)
                return False

        except Exception as e:
            print("###", e)
            # QMessageBox.information(self, "No Internet/ Server Error", "Please check your credentials/ internet connectivity")
            return False


    def SubmitData(self, data):
        config = configparser.ConfigParser()
        config.read('/home/pi/covide-module/settings.config')

        payload = {
            'plant': str(config['settings']['plant']),
            'unit': str(config['settings']['unit']),
            'zone': str(config['settings']['zone']),
            'emp_id': str(data[0]),
            'temp_in_deg': str(data[1]),
            'heart_rate': str(data[2][1]),
            'O2_saturation': str(data[2][0])
        }

        with open('/home/pi/covide-module/Log.csv', 'a+', newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow([str(data[0]), str(data[1]), str(data[2][0]), str(data[2][1]), datetime.now()])

        pid = config['settings']['plant_id']
        cid = config['settings']['companyid']
        token = self.getToken()
        
        print("this is token",token)
        url = str(config['settings']['url']) + "/1/1/employee_wellness/table_data"
        
        headers = {}
        headers['Authorization'] = 'Bearer ' + str(token)
        #'Authorization': "Token eyJraWQiOiJ3RVhjN1BxWXY2NDJJUkdVaFV1ZW1maFBLUitvNkp5WENPWUdYUVJ2M3VrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwOTNhNjIyNy1kZGVjLTQ3N2YtYjY3Yy02NTA5YWEwODQxZmQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGgtMV8yR25XWkRhSjQiLCJjb2duaXRvOnVzZXJuYW1lIjoiMDkzYTYyMjctZGRlYy00NzdmLWI2N2MtNjUwOWFhMDg0MWZkIiwib3JpZ2luX2p0aSI6ImM3YjJkZjIwLTMwNmQtNDRjYy05OWFhLWM1NGRkNGU4NmQ5MiIsImF1ZCI6IjFkc2dlMWViMGtoNWFsazdicXJmb3I4NWg4IiwiZXZlbnRfaWQiOiJmYjY5ZmEwMS02MjJkLTQ3MTEtYjkxNC1hODFmZTAwYTE0YjYiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY4OTc2MDExOSwiZXhwIjoxNjg5ODQ2NTE5LCJpYXQiOjE2ODk3NjAxMTksImp0aSI6IjRiODMxODFlLWIyY2MtNDlhMS1hZjA0LTlmMDc4OTljNGZmMiIsImVtYWlsIjoibWFkaW5lbmlAZGV0ZWN0dGVjaG5vbG9naWVzLmNvbSJ9.PXTXRw0vzfSHoyLwkAxHoxXs8HkEo_CnwbQfkV-UjmzbfvVmjPVWVpszUNvD46Swky6W1VQppBHKHPluhyS_wqQhwJnadZ0JBTGqJydGhLkDgmIESauMbLLjRzd9UPuyk83teR_V5AaXhbQfyfl83W3Yaee5SwuYGHABj_ZvrXiYsLrmt05gtNdpUbk7W8LY0m6irWN5cbtNC87EgeYAg-zxL_z1YehMWmWgmAX3k3Zwh379u7E1w6d7HV26dD4d2v1J9ueSzIKGE0IKUZaoqjVH6qzrAjqaLvixEgA2NghUD4UtDeaGNQRigYXaOT5pBBmkbiVe8LjR5Z3Qx3yaCw",
        headers['Content-Type']= 'application/json'
        

        response = requests.post(url, headers=headers, json=payload, verify=False)

        print(payload)
        print("This is url",url)
        print("response =", response.text)

#print('Given data: ', data)

if __name__ == '__main__':
    main()

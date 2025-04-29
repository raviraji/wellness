import signal
import sys
import RPi.GPIO as GPIO
import time
from temp import *
import serial
#from ble_oxy import *
from usb_oxy import *

#final
BUTTON_GPIO_1 = 8
BUTTON_GPIO_2 = 7
temp1 = 0
qr_data = ""
flag = 0
o2 = 0
pulse = 0
o2_data = []
irq = 1

def button2_pressed_callback(channel):
    print("button 2 pressed, press button 1 to begin measurement \n")
    global flag
    flag = 0

def button1_pressed_callback(channel):
    while 1:
        global flag
        if flag == 0:
            id_scan()
            flag = 1
            break
        if flag == 1:
            take_temp()
            flag = 2
            break
        if flag == 2:
            oximeter()
            flag = 3
            break
        if flag == 3:
            send_data()
            flag = 0
            break





def id_scan():
    global qr_data
    global irq
    GPIO.remove_event_detect(BUTTON_GPIO_1)
    qr_data = input("Scan your id card:  ")
    while len(qr_data) < 4 or len(qr_data) > 20:
        qr_data = input("Scan your id card:  ")
    print(qr_data + "\n")
    print("Place finger on sensor and press button 1\n ")
    flag = 1
    irq = 1

def take_temp():
    global temp1
    global irq
    temperature = temp()
    GPIO.remove_event_detect(BUTTON_GPIO_1)
    try:
        temp1 = temperature.take_temp()
        print(temp1)
    except:
        print("Coudn't take temperature readings. Check connections \n")
    print("Press button 1 to enter O2 levels \n")
    flag = 2
    irq = 1

def oximeter():
    global o2
    global pulse
    global o2_data
    global irq
    global temp1
    global qr_data

    GPIO.remove_event_detect(BUTTON_GPIO_1)
    print("Button pressed, please wait for Oxygen reading")
    try:
        o2_data = read_data()
        o2 = o2_data[0]
        pulse = o2_data[1]
        print(o2)
        print(pulse)
    except:
        pulse = 0
        o2 = 0

    if o2 == 0 or temp1 == 0 or pulse == 0 or len(qr_data) == 0:
        print("wrong measurements, press button 2 to remeasure\n")
    else:
        print("\nPress button 1 to send data\n")
    flag = 3
    irq = 1

def send_data():
    global irq
    global temp1
    global qr_data
    global o2
    global pulse

    GPIO.remove_event_detect(BUTTON_GPIO_1)
    print("Sending data")
    print("Temperature: {}".format(temp1))
    print("QR data: {} ".format(qr_data))
    print("O2: {} ".format(o2))
    print("Pulse: {}".format(pulse))
    print("data sent")
    print("press button 1 to scan your ID card")
    flag = 0
    o2 = 0
    pulse = 0
    o2_data.clear()
    irq = 1

def main():
    global irq
    print("press button 1")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_GPIO_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_2, GPIO.FALLING,
           callback=button2_pressed_callback, bouncetime=100)
    while 1:
        if irq == 1:
            GPIO.add_event_detect(BUTTON_GPIO_1, GPIO.FALLING,
                    callback=button1_pressed_callback, bouncetime=100)
            irq = 0



if __name__ == '__main__':
    main()

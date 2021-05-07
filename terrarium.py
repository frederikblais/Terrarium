#!/usr/bin/env python
import os
import glob
import time
import RPi.GPIO as GPIO

tempButton = 21
ledButton = 20
led = 24
pinDistance1 = 19
pinDistance2 = 26

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(tempButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ledButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)
    GPIO.setup(pinDistance1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pinDistance2, GPIO.IN)
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def checkDist():
    GPIO.output(pinDistance1, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(pinDistance1, GPIO.LOW)
    while not GPIO.input(pinDistance2):
        pass
    t1 = time.time()
    while GPIO.input(pinDistance2):
        pass
    t2 = time.time()
    dst = (t2-t1)*340/2
    if(dst < 0.5):
        GPIO.output(led, GPIO.LOW)
        print("Movement detected =>")
        print('Turning light on ...')
        time.sleep(5)
        print('Turning light off ...')
        print('---------------------')
        GPIO.output(led, GPIO.HIGH)

    
def ledButtonCheck():
    if GPIO.input(ledButton) == GPIO.HIGH:
        print("Button pressed =>")
        print("Turning light on ...")
        GPIO.output(led, GPIO.LOW)
        time.sleep(5)
        print('Turning light off ...')
        print('---------------------')
        GPIO.output(led, GPIO.HIGH)

def buttonCheck():
    if(GPIO.input(tempButton) == GPIO.LOW):
        return print(read_temp())
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        if(temp_c > 20):
            print("Temp Button detected =>")
            print("Temp - "+str(temp_c))
            return('---------------------')
        else:
            print("TOO COLD! - "+str(temp_c))
            print('---------------------')

# MAIN LOOP 
def loop():
    while True:
        buttonCheck()
        ledButtonCheck()
        checkDist()
        time.sleep(0.5)
        
def destroy():
    GPIO.output(led, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        GPIO.setwarnings(False)
        print('--------------------------')
        print('TERRARIUM - FREDERIK BLAIS')
        print('--------------------------')
        loop()
    except KeyboardInterrupt: 
        destroy()
        print('')
        print ('Exit ...')
        print('---------------------')
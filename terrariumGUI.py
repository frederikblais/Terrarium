#!/usr/bin/pyhton3
from tkinter import *
import os
import glob
import time
import RPi.GPIO as GPIO

led = 24
pinDistance1 = 19
pinDistance2 = 26

class Application(Frame):
    def __init__(self,master):
        GPIO.setmode(GPIO.BCM)
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        #labels
        self.tempLabel = Label (self, text = 'Current Temperature: ')
        self.tempLabel.grid(row = 0, column = 0, sticky = W)
        self.tempLabel = Label (self, text = 'Current Distance: ')
        self.tempLabel.grid(row = 3, column = 0, sticky = W)
        self.ledLabel = Label (self, text = 'Turn on LED: ')
        self.ledLabel.grid(row = 5, column = 0, sticky = W)
        
        #text boxes
        self.temp = Entry(self)
        self.temp.grid(row = 2, column = 1)
        self.dst = Entry(self)
        self.dst.grid(row = 4, column = 1)
        
        #buttons
        self.tempButton = Button(self, text = 'Get Temp', command = self.read_temp)
        self.tempButton.grid(row=2, column = 0, sticky = W)
        self.tempButton = Button(self, text = 'Get Distance', command = self.checkDist)
        self.tempButton.grid(row=4, column = 0, sticky = W)
        self.ledButton = Button(self, text = 'Turn On', command = self.led)
        self.ledButton.grid(row=6, column = 0, sticky = W)
        
    def checkDist(self):
        GPIO.setwarnings(False)
        pinDistance1 = 19
        pinDistance2 = 26
        GPIO.setup(pinDistance1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(pinDistance2, GPIO.IN)
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
        return self.dst.insert(0,str(dst))
     
    def read_temp(self):
        GPIO.setwarnings(False)
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
         
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'

        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return self.temp.insert(0,str(temp_c))
    
    def led(self):
        GPIO.setwarnings(False)
        led = 24
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.HIGH)
        GPIO.output(led, GPIO.LOW)
        time.sleep(5)
        GPIO.output(led, GPIO.HIGH)
        
root = Tk()
root.title('Terrarium')
root.geometry('340x155')
app = Application(root)
app.mainloop()
#!/usr/bin/pyhton3
from tkinter import *

class Application(Frame):
    def __int__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        self.label1 = Label (self, text='my text')
        self.label1.grid(row=0,column=0,sticky=W)
        
root = Tk()
root.title('Terrarium')
root.geometry('800x400')
app = Application(root)
app.mainloop()
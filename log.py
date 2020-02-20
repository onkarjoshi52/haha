#!/usr/bin/env python3    
import time
import serial
import os
i=0
ser = serial.Serial(             
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

while True:
    
    try:
        f=open('logs/log'+str(i)+'.txt',"r")
        if f:
            print("1")
        i+=1
    except:
        open('logs/log'+str(i)+'.txt',"w")
        print("File Created")
        break

f1=open('logs/log'+str(i)+'.txt',"a+")

for j in range(5):
    x=ser.readline()
    f1.write(x)
f1.close()

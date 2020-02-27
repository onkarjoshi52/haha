import RPi.GPIO as GPIO          #Import GPIO library
import time       
import serial               #Import time library
GPIO.setmode(GPIO.BCM)         #Set GPIO pin numbering
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
i=0
j=0
z=0

def blink(num):
    for a in range(num):
        GPIO.output(18,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(18,GPIO.LOW)
        time.sleep(0.2)
        

while True:
    
    input_state = GPIO.input(4) #Read and store value of input to a variable
    if input_state == False:     #Check whether pin is grounded
       ser = serial.Serial(
           port= '/dev/ttyUSB0',
           baudrate = z,
           parity=serial.PARITY_NONE,
           stopbits=serial.STOPBITS_ONE,
           bytesize=serial.EIGHTBITS,
           timeout=1
       )
       try:
           f=open('logs/log'+str(j)+'.txt',"r")
           if f:
               j+=1
       except:
           open('logs/log'+str(j)+'.txt',"w")

           while True:

                   f1=open('logs/log'+str(j)+'.txt',"a+")
                   x=ser.read(994)
                   f1.write(x)
                   f1.close()
                   if GPIO.input(4) == GPIO.HIGH:
                       break
           
           
    
       
           
    else:
        if GPIO.input(14) == GPIO.HIGH:
            time.sleep(1)
            n=i%8
            if n == 0:
                z=9600
                blink(n+1)
                
            elif n == 1:
                z=19200
                blink(n+1)
                
            elif n == 2:
                z=38400
                blink(n+1)
                
            elif n == 3:
                z=57600
                blink(n+1)
                
            elif n == 4:
                z=115200
                blink(n+1)
                
            elif n == 5:
                z=230400
                blink(n+1)
                
            elif n == 6:
                z=460800
                blink(n+1)
                
            elif n == 7:
                z=921600
                blink(n+1)
                
            i=i+1
 

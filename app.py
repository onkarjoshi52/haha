from guizero import *
import RPi.GPIO as GPIO
import sys
from time import sleep
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

def run(runfile):
    with open(runfile,"r") as rnf:
        exec(rnf.read())

def blank():
    s="Hold a tag near the reader"
    txt1.value=str(s)
    txt.value=""
    t1.value=""
    app.bg=None
  
def rfid():
    try:
        id, text = reader.read()
        txt.value =str(id)
        txt1.value=""
        
    finally:
        app.bg ="green"
        newid=str(id)
        newid1=newid+"  Entering Floor 1\n"
        f=open("data.txt","w")
        f.writelines(newid1)
        f.close()
        run("db.py")
        txt.after(989,blank)
        
        
        
    GPIO.cleanup()   
        

    
app = App("RFID Reader")
app.tk.attributes("-fullscreen",True)
app.tk.bind("<Escape>",exit)
app.font = "verdana"
pictue=Picture(app,image="download.png",width=1365,height=140,align="top")
txt2=Text(app,text="Asset Tracking System",size=50,width="fill", height="fill")
txt1=Text(app,text="Hold a tag near the reader",size=30,width="fill",height="fill")
txt=Text(app,size=30,width="fill",height="fill")
t1=Text(app,size=30,width="fill",height="fill")
txt.repeat(1500,rfid)
app.display()

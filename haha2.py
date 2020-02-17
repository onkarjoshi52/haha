#!/usr/bin/env python
import pymysql
import time
import RPi.GPIO as GPIO
import sys
from guizero import *
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522
from picamera import PiCamera

def blank():
    s="Hold a tag near the reader"
    txt1.value=str(s)
    txt.value=""
    t1.value=""
    app.bg=None

        
reader = SimpleMFRC522()
camera = PiCamera()


def rfid(): 
    
    try:  
        id, text = reader.read()
        #print(id)
        txt.value=str(id)
        txt1.value=""
        #time.sleep(0) 

    finally:
        
        camera.brightness = 55
        camera.image_effect = 'washedout'
        camera.awb_mode = 'sunlight'
        #time.sleep(2)
        camera.capture('image.jpg')
        #print('photo taken')
        fp = open('image.jpg','rb')
        photo = fp.read()
        
        app.bg ="green"
        newid=str(id)
        newid1=newid+"  Entering Floor 1\n"
        f=open("data.txt","w")
        f.writelines(newid1)
        f.close()
        
        db = pymysql.connect(host="192.168.43.22",user="aeron",password="arn123@",db="sample")
        cur=db.cursor()
        f=open("data.txt","r")
        data=f.readlines()
        x=len(data)
        for i in range(0,x):
            rfid=data[i].split()[0]
            floor=data[i].split()[1]
            sql="SELECT * FROM s1 WHERE RFIDTagNo = (%s) "
            cur.execute(sql,(rfid))
            fl=cur.fetchone()
            if fl == None or fl == 'Entering':
                sql="INSERT INTO s1(RFIDTagNo,AssetName,FloorNo,image) VALUES (%s,%s,%s,%s)"
                cur.execute(sql,(str(rfid),'','Entering Floor 1' ,photo))
                t1.value=" inserting New rfid"
            else :
                if fl[2] == 'Entering Floor 1' :
                    sql = "UPDATE s1 SET FloorNo = 'Exiting Floor 1' WHERE RFIDTagNo = (%s)"
                    sql1 = "UPDATE s1 SET image = (%s) WHERE RFIDTagNo = (%s)"
                    cur.execute(sql,(rfid))
                    cur.execute(sql1,(photo,rfid))
                    t1.value="Object going out"
                else :
                    sql = "UPDATE s1 SET FloorNo = 'Entering Floor 1' WHERE RFIDTagNo = (%s)"
                    sql1 = "UPDATE s1 SET image = (%s) WHERE RFIDTagNo = (%s)"
                    cur.execute(sql1,(photo,rfid))
                    cur.execute(sql,(rfid))
                    t1.value="Object coming in"
        db.commit()
        db.close()
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

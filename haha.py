#!/usr/bin/python3
import pymysql
import time
import RPi.GPIO as GPIO
import sys
import cv2
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522


#time.sleep(35)

def check_f(rfid,floor,photo):
    sql="SELECT * FROM s1 WHERE RFIDTagNo = (%s) "
    cursor.execute(sql,(rfid))
    fl=cursor.fetchone()
    if fl == None :
        print(" inserting New rfid")
        sql="INSERT INTO s1(RFIDTagNo,AssetName,FloorNo,image) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(str(rfid),'',str(floor),photo))
    else :
        if fl[2] == 'Entering Floor 1' :
            print("Object going out")
            sql = "UPDATE s1 SET FloorNo = 'Exiting Floor 1' WHERE RFIDTagNo = (%s)"
            sql1 = "UPDATE s1 SET image = (%s) WHERE RFIDTagNo = (%s)"
            cursor.execute(sql,(rfid))
            cursor.execute(sql1,(photo,rfid))
        else :
            print("Object coming in")
            sql = "UPDATE s1 SET FloorNo = 'Entering Floor 1' WHERE RFIDTagNo = (%s)"
            sql1 = "UPDATE s1 SET image = (%s) WHERE RFIDTagNo = (%s)"
            cursor.execute(sql1,(photo,rfid))
            cursor.execute(sql,(rfid))
        
reader = SimpleMFRC522()



while(1) :
    
    try:
        
        print("Hold a tag near the reader")                
        id, text = reader.read()
        print(id)
        time.sleep(1)
        
        cam = cv2.VideoCapture(0)
        ret,image = cam.read()
        time.sleep(0.5)
        cv2.imwrite('abc.jpg',image)
        cam.release()
        fp = open('abc.jpg','rb')
        photo = fp.read()
    
        
                      

    finally:
        newid=str(id)
        newid1=newid+"  Entering Floor 1\n"
        f=open("data.txt","w")
        f.writelines(newid1)
        f.close()
        
        db = pymysql.connect(host="192.168.43.22",user="aeron",password="arn123@",db="sample")
        cursor=db.cursor()
        f=open("data.txt","r")
        data=f.readlines()
        x=len(data)
        for i in range(0,x):
            rfid=data[i].split()[0]
            floor=data[i].split()[1]
            check_f(str(rfid),str(floor),photo)
        db.commit()
        db.close()
    GPIO.cleanup()
cam.stop()

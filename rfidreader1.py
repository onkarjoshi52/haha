#!/usr/bin/python3
import pymysql
import time
import RPi.GPIO as GPIO
import sys
import pygame
import pygame.camera
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

def run(runfile):
    with open(runfile,"r") as rnf:
        exec(rnf.read())
        
#time.sleep(35)

def check_f(rfid,floor):
    sql="SELECT * FROM s1 WHERE RFIDTagNo = (%s) "
    cursor.execute(sql,(rfid))
    fl=cursor.fetchone()
    if fl == None :
        print(" inserting New rfid")
        sql="INSERT INTO s1(RFIDTagNo,AssetName,FloorNo) VALUES (%s,%s,%s)"
        cursor.execute(sql,(str(rfid),'',str(floor)))
    else :
        if fl[2] == 'Entering Floor 1' :
            print("Object going out")
            sql = "UPDATE s1 SET FloorNo = 'Exiting Floor 1' WHERE RFIDTagNo = (%s)"
            cursor.execute(sql,(rfid))
        else :
            print("Object coming in")
            sql = "UPDATE s1 SET FloorNo = 'Entering Floor 1' WHERE RFIDTagNo = (%s)"
            cursor.execute(sql,(rfid))
        
reader = SimpleMFRC522()
j=0
pygame.init()
pygame.camera.init()
cameras = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cameras[0])

cam.start()

while(1) :
    
    try:
        
        print("Hold a tag near the reader")                
        id, text = reader.read()
        print(id)
        time.sleep(1)
        #run("cam.py")
        
        
        print('haha')
        image = cam.get_image()       
        pygame.image.save(image,'rpi_images/'+'PyGame_image'+str(j)+'.jpg')
        
        
        j=j+1
               

    finally:
        newid=str(id)
        newid1=newid+"  Entering Floor 1\n"
        f=open("data.txt","w")
        f.writelines(newid1)
        f.close()
        
        db = pymysql.connect(host="192.168.43.146",user="aeron",password="arn123@",db="sample")
        cursor=db.cursor()
        f=open("data.txt","r")
        data=f.readlines()
        x=len(data)
        for i in range(0,x):
            rfid=data[i].split()[0]
            floor=data[i].split()[1]
            check_f(str(rfid),str(floor))
        db.commit()
        db.close()
    GPIO.cleanup()
cam.stop()
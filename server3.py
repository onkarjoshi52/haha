import socket
import struct
import time
import serial

multicast_group = ('224.10.10.10', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(2)

f=open('baudrate.txt','r')
b=f.readline()
f.close()
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
while True:
        ser = serial.Serial(
                          
                port='/dev/ttyUSB0',
                baudrate = int(b),
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        x=ser.readline()
        print('sending {!r}'.format(x))
        sent = sock.sendto(x, multicast_group)
        
print('closing socket')
sock.close()
        

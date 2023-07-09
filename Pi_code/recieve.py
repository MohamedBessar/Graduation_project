import socket
import time
from threading import Timer
import serial

condition = ""
var1 = 't'
var2 = 'f'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.100", 5210))
print("connecion from (address) has been established")
count = 0
ser = serial.Serial(port='/dev/ttyS0',baudrate=115200,timeout = 1000)
while True:
	if ((s.recv(1024).decode("utf-8")) == "t"):
		print("Nice")
		ser.write(var1.encode())
		time.sleep(4)
		s.close()
		with open("line_follower.py") as f:
			exec(f.read())
		condition = "mohamed"
		break
	elif ((s.recv(1024).decode("utf-8")) == "f"):
		print("Not Nice")
		ser.write(var2.encode())
		time.sleep(4)
		s.close()
		#send for buzzer and twillow
		break


#if condition == "mohamed":
#		with open("line_follower.py") as f:
#			exec(f.read())

#!/usr/bin/env python3

import board
import time
import digitalio
import pwmio
import http.server
import socketserver
import sys
import signal
import os

LED_G=digitalio.DigitalInOut(board.D23)
LED_R=digitalio.DigitalInOut(board.D24)
LED_W=digitalio.DigitalInOut(board.D25)
LED_R.direction=digitalio.Direction.OUTPUT
LED_G.direction=digitalio.Direction.OUTPUT
LED_W.direction=digitalio.Direction.OUTPUT
LED_R.value=True;
LED_G.value=True;
LED_W.value=True;
MOT_L_A=pwmio.PWMOut(board.D26,frequency=25,duty_cycle=0)
MOT_L_B=pwmio.PWMOut(board.D19,frequency=25,duty_cycle=0)
MOT_R_A=pwmio.PWMOut(board.D13,frequency=25,duty_cycle=0)
MOT_R_B=pwmio.PWMOut(board.D6,frequency=25,duty_cycle=0)
oncycle = 32768
lastcommandtime = time.time()	
def setSpeeds(left,right):
	global oncycle
	if(left>0):
		if(MOT_L_A.duty_cycle != int(oncycle*left)):MOT_L_A.duty_cycle = int(oncycle*left)
		if(MOT_L_B.duty_cycle != 0):MOT_L_B.duty_cycle = 0
	else:
		if(MOT_L_A.duty_cycle != 0):MOT_L_A.duty_cycle = 0
		if(MOT_L_B.duty_cycle != int(oncycle*left*-1)):MOT_L_B.duty_cycle = int(oncycle*left*-1)
	if(right>0):
		if(MOT_R_A.duty_cycle != int(oncycle*right)):MOT_R_A.duty_cycle = int(oncycle*right)
		if(MOT_R_B.duty_cycle != 0):MOT_R_B.duty_cycle = 0
	else:
		if(MOT_R_A.duty_cycle != 0):MOT_R_A.duty_cycle = 0
		if(MOT_R_B.duty_cycle != int(oncycle*right*-1)):MOT_R_B.duty_cycle = int(oncycle*right*-1)

motMode = "S"
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		global oncycle, motMode, lastcommandtime
		# Sending an '200 OK' response
		self.send_response(200)
		# Setting the header
		self.send_header("Content-type", "text/html")
		# Whenever using 'send_header', you also have to call 'end_headers'
		self.end_headers()
		if "F" in self.path:
			motMode="F"
			lastcommandtime=time.time()
		if "B" in self.path:
			motMode="B"
			lastcommandtime=time.time()
		if "R" in self.path:
			motMode="R"
			lastcommandtime=time.time()
		if "L" in self.path:
			motMode="L"
			lastcommandtime=time.time()
		if "S" in self.path:
			motMode="S"
			lastcommandtime=time.time()
		if "X" in self.path:
			self.wfile.write(bytes("RESTARTING","utf8"))
			print("Shutting down")
			my_server._BaseServer__shutdown_request = True
			time.sleep(3)
			print("Closing")
			my_server.server_close()
			print("Restarting")
			os.execv(__file__, sys.argv)
		if "T" in self.path:
			tpos = self.path.find("T")
			pct = (1+int(self.path[tpos+1]))*10
			oncycle = int(65535*pct/100.0)
			print("Oncycle: ",oncycle)
		
		self.wfile.write(bytes("OK", "utf8"))

handler_object = MyHttpRequestHandler

PORT = 8000
my_server = False
while(not my_server):
	try:
		my_server = socketserver.TCPServer(("", PORT), handler_object)
	except:
		print("Failure to get server, retrying in 5s")
		time.sleep(5)



def quitHandler(sig, frame):
	print("Shutting down")
	my_server._BaseServer__shutdown_request = True
	print("Closing")
	my_server.server_close()
	print("Exiting")
	sys.exit(0)
	exit()

signal.signal(signal.SIGINT,quitHandler)


beat=0
def heartBeat():
	global motMode,beat,lastcommandtime
	print("beep")
	beat+=1
	if(motMode=="F"):
		setSpeeds(-1,-1)
		LED_R.value=True;
		LED_G.value=True;
		LED_W.value=((beat%4)!=0);
	if(motMode=="B"):
		setSpeeds(1,1)
		LED_W.value=True;
		LED_G.value=((beat%4)!=0);
		LED_R.value=((beat%4)!=0);
	if(motMode=="R"):
		setSpeeds(-1,0)
		LED_W.value=True;
		LED_G.value=((beat%4)!=0);
		LED_R.value=True;
	if(motMode=="L"):
		setSpeeds(0,-1)
		LED_W.value=True;
		LED_G.value=True;
		LED_R.value=((beat%4)!=0);
	if(motMode=="S"):
		LED_W.value=True;
		LED_G.value=True;
		LED_R.value=True;
		setSpeeds(0,0)
	if lastcommandtime < time.time()-10:
		setSpeeds(0,0)
		motMode="S"
		print("No command for 10 seconds, stopping")
		print(lastcommandtime)
		lastcommandtime=time.time()
		print(time.time())

my_server.service_actions = heartBeat
my_server.serve_forever()

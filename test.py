#!/usr/bin/env python3

import board
import time
import digitalio
import pwmio

MOT_L_B=pwmio.PWMOut(board.D26,frequency=1000,duty_cycle=0)
MOT_L_A=pwmio.PWMOut(board.D19,frequency=1000,duty_cycle=0)
MOT_R_B=pwmio.PWMOut(board.D13,frequency=1000,duty_cycle=0)
MOT_R_A=pwmio.PWMOut(board.D6,frequency=1000,duty_cycle=0)
oncycle = 40000

def setSpeeds(left,right):
	if(left>0):
		MOT_L_A.duty_cycle = oncycle*left
		MOT_L_B.duty_cycle = 0
	else:
		MOT_L_A.duty_cycle = 0
		MOT_L_B.duty_cycle = oncycle*left*-1
	if(right>0):
		MOT_R_A.duty_cycle = oncycle*right
		MOT_R_B.duty_cucle = 0
	else:
		MOT_R_A.duty_cycle = 0
		MOT_R_B.duty_cycle = oncycle*right*-1

while True:
	setSpeeds(0,0)
	time.sleep(1)
	setSpeeds(1,1)
	time.sleep(0.5)
	setSpeeds(0,0)
	time.sleep(1)
	setSpeeds(-1,-1)
	time.sleep(0.5)

	

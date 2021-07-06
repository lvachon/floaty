#!/usr/bin/env python3
import FaBo9Axis_MPU9250
from haversine import haversine, Unit
#from util import *
import json
import time
import math
import os
import gps

minX=126.654
maxX=163.99
minY=-36.85
maxY=8.61
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
gSession = gps.gps(host="localhost", port="2947")
gSession.stream(flags=gps.WATCH_JSON)
lastGPS = False
def getGPS():
	global lastGPS
	for report in gSession:
		if(report['class']=='TPV'):
			if(report['mode']>1):
				lastGPS=report
				return report
			return False


def compass():
        global minX, minY, maxX, maxY, mpu9250
        mag = mpu9250.readMagnet()
        if(mag['y']>maxY):maxY=mag['y']
        if(mag['y']<minY):minY=mag['y']
        if(mag['x']>maxX):maxX=mag['x']
        if(mag['x']<minX):minX=mag['x']
        if(minX==maxX or minY==maxY): return 0
        x = 2*(mag['x']-minX)/(maxX-minX) - 1
        y = 2*(mag['y']-minY)/(maxY-minY) - 1
        hdn = 90 - 180.0 * math.atan2(x,y)/math.pi
        if(hdn<0):hdn+=360
        if(hdn>360):hdn-=360
        return hdn

def bearingToPoint(srcLat,srcLon,destLat,destLon):
	srcLat*=math.pi/180.0
	srcLon*=math.pi/180
	destLat*=math.pi/180
	destLon*=math.pi/180
	x = math.cos(destLat)*math.sin(destLon-srcLon)
	y = math.cos(srcLat)*math.sin(destLat)-math.sin(srcLat)*math.cos(destLat)*math.cos(destLon-srcLon)
	b = 180 * math.atan2(x,y)/math.pi
	if(b<0):b+=360
	return b

def autopilot():
	global waypoints, currentWaypoint, status, settings
	gps = getGPS()
	if(gps==False):
		print("No GPS")
		return "S"
	heading = compass()
	readWaypoints()
	if(len(waypoints)<1):
		print("No waypoints")
		return "S"
	dist = haversine((gps['lat'],gps['lon']),(waypoints[currentWaypoint][0],waypoints[currentWaypoint][1]),Unit.METERS)
	status['dist']=int(dist*10)/10
	status['heading']=int(heading*10)/10
	status['target']=currentWaypoint
	if(gps['hdop']<3):
		if(dist<3*gps['hdop']):
			print("At waypoint")
			if(currentWaypoint+1<len(waypoints)):
				print("Going to next one")
				currentWaypoint+=1
			else:
				print("Going to first one")
				currentWaypoint=0
		else:
			desiredBearing = bearingToPoint(gps['lat'],gps['lon'],waypoints[currentWaypoint][0],waypoints[currentWaypoint][1])
			bearingDiff = desiredBearing - heading
			if(bearingDiff>180):bearingDiff-=360
			if(bearingDiff<-180):bearingDiff+=360
			if(bearingDiff>90): return "R"
			if(bearingDiff<-90): return "L"
			if(bearingDiff>30): return "FR"
			if(bearingDiff<-30): return "FL"
			return "F"
	else:
		print("Too innacurate to move")
		return "S"


waypoints = [(42.107582,-71.034714),(42.107684,-71.034672)] 
currentWaypoint = 0

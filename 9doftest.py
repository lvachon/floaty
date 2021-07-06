import FaBo9Axis_MPU9250
import time
import sys
import math
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
#126.654 163.99 -36.85 8.61
minX=126.654
maxX=163.99
minY=-36.85
maxY=8.61
mag = 0
def compass():
	global minX
	global minY
	global maxX
	global maxY
	global mag
	mag = mpu9250.readMagnet()
	if(mag['z']>maxY):maxY=mag['z']
	if(mag['z']<minY):minY=mag['z']
	if(mag['x']>maxX):maxX=mag['x']
	if(mag['x']<minX):minX=mag['x']
	if(mag['x']==0 or mag['z']==0): return 0
	if(minX==maxX or minY==maxY): return 0
	x = 2*(mag['x']-minX)/(maxX-minX) - 1
	y = 2*(mag['z']-minY)/(maxY-minY) - 1
	#x = mag['x']
	#y = mag['y']
	hdn = 90 - 180.0 * math.atan2(x,y)/math.pi
	if(hdn<0):hdn+=360
	if(hdn>360):hdn-=360
	return hdn

try:
    while True:
        print(" heading = ", (compass()))
        print(minX,maxX,minY,maxY)
        time.sleep(0.25)

except KeyboardInterrupt:
    sys.exit()

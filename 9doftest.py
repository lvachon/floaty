import FaBo9Axis_MPU9250
import time
import sys
import math
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

#18.221 62.345 48.369 90.085
minX=18.221
maxX=62.345
minY=48.369
maxY=90.085

def compass():
	global minX
	global minY
	global maxX
	global maxY
	mag = mpu9250.readMagnet()
	if(mag['y']>maxY):maxY=mag['y']
	if(mag['y']<minY):minY=mag['y']
	if(mag['x']>maxX):maxX=mag['x']
	if(mag['x']<minX):minX=mag['x']
	if(minX==maxX or minY==maxY): return 0
	x = 2*(mag['x']-minX)/(maxX-minX) - 1
	y = 2*(mag['y']-minY)/(maxY-minY) - 1
	hdn = 180.0 * math.atan2(x,y)/math.pi - 90
	if(hdn<0):hdn+=360
	return hdn

try:
    while True:
        print(" heading = ", (compass()))
        time.sleep(0.5)

except KeyboardInterrupt:
    sys.exit()

import io
import time
import picamera
import cv2
import numpy as np
import RPi.GPIO as GPIO ## Import GPIO library
import sys
#sys.stdout = open('log.txt', 'w')


GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

GPIO.output(7,False)

camera = picamera.PiCamera()

maxScans = 10000
scanNum = 0

stream = io.BytesIO()
time.sleep(2) #initial camera start up

startScanTime = time.time()
while(scanNum < maxScans):
    print "Getting pic"
    camera.capture(stream, format='jpeg')
    
    # Construct a numpy array from the stream
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of orange color in HSV
    #h=5-15
    #s=180-190
    #v=230-250

    lower_orange = np.array([0,100,100])
    upper_orange = np.array([15,255,255])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    edges = cv2.Canny(mask,50,150,apertureSize = 3)

    lines = cv2.HoughLines(edges,1,np.pi/180,55)

    if lines is not None:
        print "line count: " + str(len(lines[0]))

    lowerAngle = 26
    upperAngle = 44

    starAngleCount = 0
    if lines != None and len(lines) > 0:
        for rho1,theta in lines[0]:
            theta = theta/np.pi*180
            if starAngleCount < 4:
                for rho2,phi in lines[0]:
                    phi = phi/np.pi*180
                    angle = 0
                    complement = 180 - angle
                    if rho1 > 0 and rho2 > 0:
                        angle = 180 - abs(theta - phi)
                        complement = 180 - angle
                    elif rho1 < 0 and rho2 > 0:
                        phiPrime = 180 - phi
                        angle = 180 - theta - phiPrime
                        complement = 180 - angle
                    elif rho1 > 0 and rho2 < 0:
                        thetaPrime = 180 - theta
                        angle = 180 - thetaPrime - phi
                        complement = 180 - angle
                    elif rho1 < 0 and rho2 < 0:
                        angle = 180 - abs(theta - phi)
                        complement = 180 - angle
                    #print angle
                    if (angle < upperAngle and angle > lowerAngle) or (complement > lowerAngle and complement < upperAngle):
                        print angle
                        starAngleCount += 1
                        break

    print "starAngleCount: " + str(starAngleCount/2)



    # Scanning by pixel count

    # count = np.sum(mask)/255

    # # Currently checking just by count of pixels matched
    # # TODO by shape
    # print "count: " + str(count)
    # if count > 1000000/255:
    #     print "Found it!"
    # else:
    #     print "Not found"

    if starAngleCount > 1:
        GPIO.output(7,True)
        print "Found it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else:
        GPIO.output(7,False)
        print "Not found"

    print "Scans: " + str(scanNum+1)
    
    #time.sleep(1)
    
    scanNum += 1
    stream = io.BytesIO()
loopTime = time.time() - startScanTime
print loopTime    













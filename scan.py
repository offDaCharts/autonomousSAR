import io
import time
import picamera
import cv2
import numpy as np

camera = picamera.PiCamera()

maxScans = 20
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
    lower_orange = np.array([0,120,50])
    upper_orange = np.array([30,250,250])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    count = np.sum(mask)/255

    # Currently checking just by count of pixels matched
    # TODO by shape
    print "count: " + str(count)
    if count > 1000000/255:
        print "Found it!"
    else:
        print "Not found"

    print "Scans: " + str(scanNum)
    #time.sleep(0.5)
    scanNum += 1
    stream = io.BytesIO()
loopTime = time.time() - startScanTime
print loopTime    













import io
import time
import picamera
import cv2
import numpy as np
import sys

print sys.argv[1]

image = cv2.imread(sys.argv[1])
print len(image)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of orange color in HSV
lower_orange = np.array([0,120,50])
upper_orange = np.array([30,250,250])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_orange, upper_orange)

print time.time()
count = np.sum(mask)
print count/255
print time.time()

# Bitwise-AND mask and original image
res = cv2.bitwise_and(image,image, mask= mask)


cv2.imwrite('frame.png',image)
cv2.imwrite('mask.png',mask)
cv2.imwrite('res.jpg',res)



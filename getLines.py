import cv2
import numpy as np
import sys

# print sys.argv[1]
# img = cv2.imread(sys.argv[1], 0)

img = cv2.imread("mask.png", 0)

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#mask.png is already binary
edges = cv2.Canny(img,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,50)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(100,255,255),2)

cv2.imwrite('houghlines3.jpg',img)

lowerAngle = 26
upperAngle = 44

starAngleCount = 0
for rho1,theta in lines[0]:
    theta = theta/np.pi*180
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
        print angle
        print complement
        print " "
        if (angle < upperAngle and angle > lowerAngle) or (complement > lowerAngle and complement < upperAngle):
            starAngleCount += 1

print "starAngleCount: " + str(starAngleCount/2)





#!/usr/bin/python
import cv
import cv2

cv.NamedWindow('a_window',cv.CV_WINDOW_AUTOSIZE)

image = cv.LoadImage('round-black.jpg')
storage = cv.CreateMemStorage()
classifier = "haarcascade_frontalface_alt.xml"
classB = "haarcascade_mcs_mouth.xml"

har=cv.Load(classifier)
haar=cv.Load(classB)
detected = cv.HaarDetectObjects(image, har, storage, 1.1, 2,cv.CV_HAAR_DO_CANNY_PRUNING)


if detected:
	for ((x,y,h,w), neigh) in detected:
		cv.Rectangle(image,(x,y), (x+h,y+w),(255,255,255))
		sub=cv.GetSubRect(image, (x,y,h,w))
		#sub2=cv.GetSubRect(, (x,y,h,w))
		detected2 = cv.HaarDetectObjects(sub, haar, storage, 1.1, 2,cv.CV_HAAR_DO_CANNY_PRUNING)
	for ((x,y,h,w), neigh) in detected2:
		cv.Rectangle(sub,(x,y), (x+h,y+w),(0,0,255))

cv.NamedWindow("result")
cv.ShowImage("result",sub)

#cv.NamedWindow("result2")
#cv.ShowImage("result2",sub2)

cv.ShowImage('a_window',image)
cv.WaitKey(1000000)

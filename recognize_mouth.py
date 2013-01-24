#!/usr/bin/python
import cv
import cv2

image = cv.LoadImage('img8.jpeg')
storage = cv.CreateMemStorage()
classifier_face = "haarcascade_frontalface_alt.xml"
classifier_mouth = "haarcascade_mcs_mouth.xml"

haar_face = cv.Load(classifier_face)
haar_mouth = cv.Load(classifier_mouth)
faces = cv.HaarDetectObjects(image, haar_face, storage, 1.1, 2,cv.CV_HAAR_DO_CANNY_PRUNING)

# S'il y a des visages detectes :
if faces :
# Pour chaque visage detecte:
# x,y : coord debut du rectangle.
	# neigh : % de "surete"
	for ((x,y,largeur,hauteur), neigh) in faces:
# Creation du rectangle pour situer le visage.
		cv.Rectangle(image,(x,y), (x+largeur,y+hauteur),(255,255,255))
		l_1_quart = largeur/4
		h_1_5eme = hauteur/5
		img_mouth = cv.GetSubRect(image, (x+l_1_quart,y+3*h_1_5eme,2*l_1_quart,2*h_1_5eme))
		mouths = cv.HaarDetectObjects(img_mouth, haar_mouth, storage, 1.1, 2,cv.CV_HAAR_DO_CANNY_PRUNING)

# S'il y a des bouches detectees
	if mouths :
		for ((x,y,l,h), neigh) in mouths:
			cv.Rectangle(img_mouth, (x,y), (x+l,y+h), (0,0,255))
		cv.NamedWindow("Mouth")
		cv.ShowImage("Mouth",img_mouth)

	cv.NamedWindow("Face")
	cv.ShowImage("Face",image)


cv.WaitKey(1000000)

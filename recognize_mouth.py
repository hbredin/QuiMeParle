#!/usr/bin/python
import cv
import cv2
import sys

def bouche(nom_img) :
	image = cv.LoadImage('faceDatabase/BioID-FaceDatabase-V1.2/'+nom_img)
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
			# Puis on essaie de situer la bouche dans le visage pour eviter les erreurs :
			# 0.287068965517 = pourcentage ou est situe au max la bouche a gauche
			# 0.64 = pourcentage ou est situe au max la bouche en hauteur
			# 0.48706817733999996 = 0.744137142857-0.257068965517 ou 0.744137142857 endroit max de la bouche a droite
			# 0.3501875 = 0.9901875-0.64 ou 0.9901875 endroit max de la bouche en bas
			img_mouth = cv.GetSubRect(image, (x+int(largeur*0.287068965517),y+int(hauteur*0.64),
							  int(largeur*0.48706817733999996),int(hauteur*0.3501875) ))
			mouths = cv.HaarDetectObjects(img_mouth, haar_mouth, storage, 1.1, 2, cv.CV_HAAR_DO_CANNY_PRUNING)
			
	# S'il y a des bouches detectees
		if mouths :
			for ((x,y,l,h), neigh) in mouths:
				cv.Rectangle(img_mouth, (x,y), (x+l,y+h), (0,0,255))
			cv.NamedWindow("Mouth")
			cv.ShowImage("Mouth", img_mouth)

		cv.NamedWindow("Face")
		cv.ShowImage("Face", image)


	cv.WaitKey(1000000)

if __name__ == '__main__' :
	bouche(sys.argv[1])

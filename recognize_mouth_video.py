#!/usr/bin/python
import cv
import cv2
import sys

# Initialisation des fichiers a vide.
fichier_visage = open('visage.txt', 'a')
fichier_bouche = open('bouche.txt', 'a')
fichier_video = "VIDEOTEST"


def ecrit_position(visage, compteur, x, y, largeur, hauteur) :
	# Attention : visage = true si on ecrit dans visage_nomDeLaVideo, sinon bouche_nomDeLaVideo.
	if visage :
		fichier_visage.write('img n: '+str(compteur)+'; ('+str(x)+','+str(y)+'); '+str(largeur)+'*'+str(hauteur)+'\n')
	else :
		fichier_bouche.write('img n: '+str(compteur)+'; ('+str(x)+','+str(y)+'); '+str(largeur)+'*'+str(hauteur)+'\n')

def bouche(image, compteur) :
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
			# Image detectee -> sauvegarde position :
			ecrit_position(True, compteur, x, y, largeur, hauteur)

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
				# Image detectee -> sauvegarde position :
				ecrit_position(False, compteur, x, y, l, h)

				cv.Rectangle(img_mouth, (x,y), (x+l,y+h), (0,0,255))
			cv.NamedWindow("Mouth")
			cv.ShowImage("Mouth", img_mouth)

		cv.NamedWindow("Face")
		cv.ShowImage("Face", image)

	cv.WaitKey(1)


def affiche_bouche(video) :
	compteur_de_frame = 0
	
	capture = cv.CreateFileCapture(video)
	
	image = cv.QueryFrame(capture)

	while True :
		print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
		bouche(image, compteur_de_frame)
		compteur_de_frame = compteur_de_frame + 1
		image = cv.QueryFrame(capture)
		print compteur_de_frame
		print 'on est dans le while'



if __name__ == '__main__' :
	print 'on entre dans le main..!'
	fichier_visage.write('Numero Image; (posX, posY); largeur*hauteur\n')
	fichier_bouche.write('Numero Image; (posX, posY); largeur*hauteur\n')
	
	affiche_bouche(fichier_video)
	print 'sortie affiche_bouche.'

	fichier_visage.close()
	fichier_bouche.close()

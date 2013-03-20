#!/usr/bin/python
import cv, cv2, sys, numpy, os
import montre_nuance_gris as mng
import matplotlib.pyplot as plt
import parle as parle


# Definition : va ecrire dans f.txt
def ecrit_position(texte, f) :
	f.write(texte)
	f.flush()


# Avec une image, retrouve la position de la bouche, puis fait appel a ecrit_position pour garder la position de la bouche sur l'image numero compteur.
def bouche(image, compteur, fichier_visage, fichier_bouche) :
	storage = cv.CreateMemStorage()
	classifier_face = "haarcascade_frontalface_alt.xml"
	classifier_mouth = "haarcascade_mcs_mouth.xml"

	haar_face = cv.Load(classifier_face)
	haar_mouth = cv.Load(classifier_mouth)
	faces = cv.HaarDetectObjects(image, haar_face, storage, 1.1, 2,cv.CV_HAAR_DO_CANNY_PRUNING)

	# Il ne peut y avoir qu'une seule bouche dans un visage : on prendra le cadre le plus important.
	l_max = 0
	h_max = 0
	# Il faut garder en memoire l'emplacement du meilleur rectangle_bouche quand on parcourt toutes les bouches
	x_bouche = 0
	y_bouche = 0

	# S'il y a des visages detectes :
	if faces :
		# Pour chaque visage detecte:
		# x,y : coord debut du rectangle.
		# neigh : % de "surete"
		for ((x,y,largeur,hauteur), neigh) in faces:
			# Image detectee -> sauvegarde position :
			ecrit_position(str(compteur)+' '+str(x)+' '+str(y)+' '+str(largeur)+' '+str(hauteur)+' \n', fichier_visage)

			# Creation du rectangle pour situer le visage.
			cv.Rectangle(image,(x,y), (x+largeur,y+hauteur),(255,255,255))
			# Puis on essaie de situer la bouche dans le visage pour eviter les erreurs :
			# 0.287068965517 = pourcentage ou est situe au max la bouche a gauche
			# 0.64 = pourcentage ou est situe au max la bouche en hauteur
			# 0.48706817733999996 = 0.744137142857-0.257068965517 ou 0.744137142857 endroit max de la bouche a droite
			# 0.2501875 = 0.9901875-0.74 ou 0.9901875 endroit max de la bouche en bas
			img_mouth = cv.GetSubRect(image, (x+int(largeur*0.287068965517),y+int(hauteur*0.74),
							  int(largeur*0.48706817733999996),int(hauteur*0.2501875) ))
			mouths = cv.HaarDetectObjects(img_mouth, haar_mouth, storage, 1.1, 2, cv.CV_HAAR_DO_CANNY_PRUNING)
			
	# S'il y a des bouches detectees
		if mouths :
			for ((x,y,l,h), neigh) in mouths:
				if l*h > l_max*h_max :
					l_max = l
					h_max = h
					x_bouche = x
					y_bouche = y

			# Image detectee -> sauvegarde position :
			ecrit_position(str(compteur)+' '+str(x_bouche)+' '+str(y_bouche)+' '+str(l_max)+' '+str(h_max)+' \n', fichier_bouche)
			cv.Rectangle(img_mouth, (x,y), (x+l,y+h), (0,0,255))
			# Reinitialise les parametres de test pour la prochaine image :
			l_max = 0
			h_max = 0

			cv.NamedWindow("Mouth")
			cv.ShowImage("Mouth", img_mouth)

		cv.ShowImage("Face", image)
		cv.NamedWindow("Face")

	cv.WaitKey(1)


# definition : fait defiler les images une a une d'une video pour travailler dessus.
def affiche_bouche(video, fichier_visage=None, fichier_bouche=None) :
	compteur_de_frame = 0
	cap = cv.CreateFileCapture(video)
	image = cv.QueryFrame(cap)

	while image != None :
		#print str(cv.GetSize(image))+'\n'
		bouche(image, compteur_de_frame, fichier_visage, fichier_bouche)
		compteur_de_frame += 1
		# Image suivante.
		image = cv.QueryFrame(cap)
		print compteur_de_frame
		#print 'on est dans le while'


# va redimensionner toutes les images des bouches de facon uniforme pour pouvoir comparer frame par frame ensuite.
def resize_uniforme(l) :
	largeur = 0
	hauteur = 0
	liste = []
	for img in l :
		if largeur < img.width :
			largeur = img.width
		if hauteur < img.height :
			hauteur = img.height

	for img in l :
		i = cv.CreateImage((largeur, hauteur), 8, 1)
		cv.Resize(img, i)
		liste.append(i)

	return liste

# Retourne vrai si l'extention du fichier equivaut a /      <=>       C'est un dossier
def is_file(_str) :
	return _str[-1] == '/'
# Retourne vrai si l'extention du fichier equivaut a .avi
def is_avi(_str) :
	return _str[-3:-1]+_str[-1] == 'avi'

# Va faire tourner le programme pour toutes les videos du corpus
def forall_video(empl = 'Document/QuiMeParle/QuiMeParle_videos/') :
	# Recupere tous les fichiers du corpus : video+audio
	fich = os.listdir(empl)
	# Permet de recuperer uniquement les videos
	fich = filter(is_avi, fich)
	for it in fich :
		parle_ou_pas(empl+it)



# Pour une image donnee, va sommer la nuance grise des pixels pour en faire une moyenne.
# bouche = image
# moyenne = [Moyenne, Compteur_moyenne]
def nv_gris(bouche) :
    moy = 0
    h, l = cv.GetSize(bouche)

    for i in range(l) :
        for j in range(h) :
            #print 'i,j : '+str(i)+','+str(j)
            #print str(range(l))+' '+str(range(h))
            #print str(bouche[i,j])
            moy += bouche[i,j]
            
    print "\n Nouvelle image\n"
    print "moy : "+str(moy)+"; longueur : "+str(l)+"; hauteur : "+str(h)+"; => "+str(moy/(l*h))+"\n"
    # resultat moyen du pixel. nombre_de_pixel = l*h
    return (moy / (l*h))
    #print "#########################################\n"
    #for v in range(len(moyenne)) :
      #  print moyenne[i]+"\n"
    

# Fais tourner l'algo pour une video donnee
def parle_ou_pas(empl_video) :
	print 'Debut : main...'
	# Variables de parle.py, utile pour l'appel de la fonction pixel_parle
	moyenne = 0.0
	compt_m = 0
	
	# Initialisation des fichiers texte.
	# /!\ le sys.argv[1] est du type : 'dossier/name.avi'
	name = empl_video.split('.')[0].split('/')[1]
	fichier_visage = open('placement_visage/'+name+'_visage.txt', 'w')
	fichier_bouche = open('placement_bouche/'+name+'_bouche.txt', 'w')
	
	fichier_visage.write('Numero_image posX posY largeur hauteur\n')
	fichier_bouche.write('Numero_image posX posY largeur hauteur\n')
	fichier_visage.close()
	fichier_bouche.close()

	fichier_visage = open('placement_visage/'+name+'_visage.txt', 'a')
	fichier_bouche = open('placement_bouche/'+name+'_bouche.txt', 'a')
	print '\tDebut : affiche_bouche...'
	affiche_bouche(empl_video, fichier_visage, fichier_bouche)
	print '\t...Fin : affiche_bouche.'

	fichier_visage.write('end')
	fichier_bouche.write('end')
	fichier_visage.close()
	fichier_bouche.close()
	
	print '\tDebut : lecture...'
	liste_des_bouches = []
	parle.rgb_to_gray(name, cv.CreateFileCapture(empl_video), liste_des_bouches)
	print '\t...Fin : lecture'

	print "###\n\n Liste des images BOUCHES"
	#print liste_des_bouches
	print "\n\n"
	print "###\n"

	liste_des_bouches = resize_uniforme(liste_des_bouches)

	print "###\n\n Liste des images BOUCHES"
	print liste_des_bouches
	print "\n\n"
	print "###\n"
	liste_des_bouches_nv_gris = []

	for i in liste_des_bouches :
		print i
		print "boubou : \n"
		liste_des_bouches_nv_gris.append(nv_gris(i))

	
	print liste_des_bouches_nv_gris



	print '\tDebut : affichage graphique :\n'
	plt.plot(liste_des_bouches_nv_gris)
	plt.show()
	print '/tFin : affichage graphique\n'
	print '...Fin : main'
	print ' ***************MANQUE A METTRE LE GRAPHIQUE EN IMAGE********************** '
	print '\n'
	

if __name__ == '__main__' :
	print is_avi(sys.argv[1])
	if (is_avi(sys.argv[1])) :
		parle_ou_pas(sys.argv[1])

	elif (is_file(sys.argv[1])) :	
		# donner le dossier en chemin absolu en parametre. fais tourner l'algo pour toutes les videos
		forall_video(sys.argv[1])

	else :
		forall_video()

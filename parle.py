import cv, cv2, sys

# Pour une image donnee, va sommer la nuance grise des pixels pour en faire une moyenne.
# bouche = image
# moyenne = [Moyenne, Compteur_moyenne]
def pixel_parle(bouche, moyenne) :
    moy = 0
    h, l = cv.GetSize(bouche)

    for i in range(l) :
        for j in range(h) :
            #print 'i,j : '+str(i)+','+str(j)
            #print str(range(l))+' '+str(range(h))
            #print str(bouche[i,j])
            moy += bouche[i,j]
    
    # resultat moyen du pixel. nombre_de_pixel = l*h
    moyenne.append(moy / (l*h))
    #print "#########################################\n"
    #for v in range(len(moyenne)) :
      #  print moyenne[i]+"\n"




def lecture(fichier, capture, moyenne) :
    # Premiere image de la capture et initialisation des variables temporaires.
    img = cv.QueryFrame(capture)
    numero_img = -1
    x = -1
    y = -1
    largeur = -1
    hauteur = -1
    mot = ''
    
    f = open(fichier, 'r')
    # readline() + readline() car on ne prend pas en compte la ligne de commentaire de bouche.txt
    f.readline()

    mot = f.readline().split(' ')

    print "\t\t...Debut fichier bouche.txt\n"
    while mot[0] != 'end' :
        # 8 => 2^8 ?   ||   1 = nombre de canaux couleur ouverts => only gray. (3=RGB)...
        dest_img = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.CvtColor(img, dest_img, cv2.COLOR_BGR2GRAY)

        # Recupere les valeurs d'une ligne.
        numero_img = int(mot[0])
        x = int(mot[1])
        y = int(mot[2])
        largeur = int(mot[3])
        # Petite feinte : il faut enlever le \n restant grace a rstrip.
        hauteur = int(mot[4].rstrip('\n'))
        
        # Parmis l'image, on recupere la bouche.
        bouche = cv.GetSubRect(dest_img, (x,y,largeur,hauteur))
        # Parle ou pas ? fonction qui va servir a determiner si c'est good ou pas, selon peut etre des variables globales (precedente img)
        pixel_parle(bouche, moyenne)

        # Si la ligne suivante correspond a la meme frame, on reboucle sur la meme image.
        mot = f.readline().split(' ')
        
        try : 
            if int(mot[0]) != numero_img :
                # Passe a l'image.
                img = cv.QueryFrame(capture)
        except ValueError : 
            print "\t\t...Fin fichier bouche.txt\n"
            
        


if __name__ == '__main__' :
    # Recupere la video et la passe en parametre
    print 'Debut...\n'
    moyenne = []
    lecture('bouche.txt', cv.CreateFileCapture(sys.argv[1]), moyenne)
    print '...Fin\n'

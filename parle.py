import cv, cv2, sys, numpy

def rgb_to_gray(name, capture, liste_des_bouches) :
    # Premiere image de la capture et initialisation des variables temporaires.
    img = cv.QueryFrame(capture)
    numero_img = -1
    x = -1
    y = -1
    largeur = -1
    hauteur = -1
    mot = ''
    moyenne = []
    
    f = open('placement_bouche/'+name+'_bouche.txt', 'r')
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
        
        # Parmis l'image, on recupere la bouche, en niveau de gris
        bouche = cv.GetSubRect(dest_img, (x,y,largeur,hauteur))

        liste_des_bouches.append(bouche)
        # Si la ligne suivante correspond a la meme frame, on reboucle sur la meme image.
        mot = f.readline().split(' ')
        
        try : 
            if int(mot[0]) != numero_img :
                # Passe a l'image suivante.
                img = cv.QueryFrame(capture)
        except ValueError : 
            print "\t\t...Fin fichier bouche.txt\n"
            
        
    #Pour Pierre : ecriture dans un fichier des sommes des pixels en hauteur de gris.
    numpy.savetxt('donneesFormat/'+name+'.datV', moyenne)








if __name__ == '__main__' :
    # Recupere la video et la passe en parametre
    print 'Debut...\n'
    moyenne = []
    lecture('bouche.txt', cv.CreateFileCapture(sys.argv[1]), moyenne)
    print '...Fin\n'

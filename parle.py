import cv
import sys

# DANS L'ETAT ACTUEL, IL N'Y A QU'UNE MOYENNE DES COULEURS DES PIXELS. IL FAUDRAIT DETERMINER SI MOYENNE BAISSE BEAUCOUP AU FUR ET A MESURE.

moyenne = 0.0
compt_m = 0


def pixel_parle(bouche) :
    # r , g ou b proche de 0 => noir
    r = -1
    g = -1
    b = -1
    l, h = cv.GetSize(bouche)

    for i in range(l) :
        for j in range(h) :
            r,g,b = bouche[i,j]
            moyenne += r + g + b
            compt_moy += 3
            print str(bouche[i,j])+'\n'
    
    # resultat moyen du pixel.
    moy /= compt_moy
    # Il ne reste plus qu'une valeur dans la moyenne
    compt_moy = 1




def lecture(fichier, capture) :
    print '\tdebut lecture...\n'
    # Premiere image de la capture et initialisation des variables.
    image = cv.QueryFrame(capture)
    numero_img = -1
    x = -1
    y = -1
    largeur = -1
    hauteur = -1
    i = 0
    
    fich = open(fichier+'.txt', 'r')
    # Tout le fichier est dans ligne sous forme d'un string.
    ligne = fich.read()
    # lignes = tableau des valeurs qui s'enchainent : numero img, x, y, larg, haut.
    lignes = ligne.split(' ')
    
    while lignes[i] != 'end' :
        # Recupere les valeurs d'une ligne.
        # str(compteur)+' '+str(x)+' '+str(y)+' '+str(largeur)+' '+str(hauteur)+'\n'
        numero_img = int(lignes[i])
        x = int(lignes[i+1])
        y = int(lignes[i+2])
        largeur = int(lignes[i+3])
        hauteur = int(lignes[i+4])
        
        # Parmis l'image, on recupere la bouche.
        bouche = cv.GetSubRect(image, (x,y,largeur,hauteur))
        # Parle ou pas ? fonction qui va servir a determiner si c'est good ou pas, selon peut etre des variables globales (precedente img)
        pixel_parle(bouche)

        # Passe a l'image et ligne suivante.
        image = cv.QueryFrame(capture)
        i = i + 5

    print '\t...fin lecture\n'



if __name__ == '__main__' :
    # Recupere la video et la passe en parametre
    print 'Debut...\n'
    lecture('bouche', cv.CreateFileCapture(sys.argv[1]))
    print '...Fin\n'

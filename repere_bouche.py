import cv
import Image

# Retourne 4 tableaux correspondant a :
# x1 : pourcentage du placement de la bouche extreme gauche
# y1 : pourcentage du placement de la bouche extreme haut
# x2 : pourcentage du placement de la bouche extreme droit
# y2 : pourcentage du placement de la bouche extreme bas
def rectangle_bouche() :
    classifier = "haarcascade_frontalface_alt.xml"
    haar = cv.Load(classifier)
    storage = cv.CreateMemStorage()

    deb_bouche_x = 100
    deb_bouche_y = 100
    fin_bouche_x = 0
    fin_bouche_y = 0

    # Pourcentage du carre bouche par rapport au visage.
    # x1,y1 = coin superieur/gauche
    # x2,y2 = coin inferieur/droit
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    compteur = 0
    compteur_s = ''
    
    while compteur < 1521 :
        # On charge le fichier texte pour recuperer les valeurs qui delimite la bouche
        compteur_s = str(compteur)
        if compteur < 10 :
            fich_txt = 'faceDatabase/points_20/bioid_000'+compteur_s+'.pts'
            fich_img = 'faceDatabase/BioID-FaceDatabase-V1.2/BioID_000'+compteur_s+'.pgm'
        elif compteur < 100 :
            fich_txt = 'faceDatabase/points_20/bioid_00'+compteur_s+'.pts'
            fich_img = 'faceDatabase/BioID-FaceDatabase-V1.2/BioID_00'+compteur_s+'.pgm'
        elif compteur < 1000 :
            fich_txt = 'faceDatabase/points_20/bioid_0'+compteur_s+'.pts'
            fich_img = 'faceDatabase/BioID-FaceDatabase-V1.2/BioID_0'+compteur_s+'.pgm'
        else  :
            fich_txt = 'faceDatabase/points_20/bioid_'+compteur_s+'.pts'
            fich_img = 'faceDatabase/BioID-FaceDatabase-V1.2/BioID_'+compteur_s+'.pgm'
        fichier = open(fich_txt, 'r')
        ligne = fichier.readlines()
        deb_x,_ = ligne[5].split(' ')
        _,deb_y = ligne[20].split(' ')
        fin_x,_ = ligne[6].split(' ')
        _,fin_y = ligne[21].split(' ')

        # string -> float
        deb_x = float(deb_x)
        deb_y = float(deb_y)
        fin_x = float(fin_x)
        fin_y = float(fin_y)

        # On charge l'image pour recuperer la taille (x,y) du visage
        img = cv.LoadImage(fich_img)
        face = cv.HaarDetectObjects(img, haar, storage, 1.1, 2, cv.CV_HAAR_DO_CANNY_PRUNING)
        print cv.HaarDetectObjects(img, haar, storage, 1.1, 2, cv.CV_HAAR_DO_CANNY_PRUNING)
        print 'JE RENTRE DANS FACE : '
        if face :
            print 'J\'Y SUIS. Fichier numero '+str(compteur)
            ((x,y, l,h), neigh) = face[0]
            # Puis on recentre l'image en fonction du visage pour calculer
            largeur = float(l)
            hauteur = float(h)
            print '('+str(deb_x)+','+str(deb_y)+') -> ('+str(fin_x)+','+str(fin_y)+')    avec (x:'+str(x)+', y:'+str(y)+')'
            deb_x = deb_x - float(x)
            fin_x = fin_x - float(x)
            deb_y = deb_y - float(y)
            fin_y = fin_y - float(y)
            print '('+str(deb_x)+','+str(deb_y)+') -> ('+str(fin_x)+','+str(fin_y)+')'

            if deb_x > 0 and deb_y > 0 and fin_x > 0 and fin_y > 0 :
                # Enfin on travaille pour avoir le % minimum (x1,y1)
                # et le maximum (x2,y2) par rapport a l'image :
                x1.append(deb_x/largeur)
                y1.append(deb_y/hauteur)
                x2.append(fin_x/largeur)
                y2.append(fin_y/hauteur)

#                if deb_bouche_x > (deb_x/largeur) :
#                    deb_bouche_x = deb_x/largeur
        
#                if deb_bouche_y > (deb_y/hauteur) :
#                    deb_bouche_y = deb_y/hauteur
            
#                if fin_bouche_x < (fin_x/largeur) :
#                    fin_bouche_x = fin_x/largeur
                
#                if fin_bouche_y < (fin_y/hauteur) :
#                    fin_bouche_y = fin_y/hauteur
                    
        resultat = open('faceDatabase/resultat/bordure_bouche_max.txt', 'a')
        resultat.write('fichier numero :'+str(compteur)+'\n')
        resultat.write('pourcentage 1er point  : x='+str(deb_bouche_x)+' y='+str(deb_bouche_y)+'\n')
        resultat.write('pourcentage 2eme point : x='+str(fin_bouche_x)+' y='+str(fin_bouche_y)+'\n\n')

        compteur = compteur + 1

        resultat.close()
        fichier.close()

        print 'coin first (x,y) : ('+str(deb_bouche_x)+', '+str(deb_bouche_y)+')'
        print 'coin last (x,y) : ('+str(fin_bouche_x)+', '+str(fin_bouche_y)+') \n'
    
    return (x1,y1,x2,y2)


# Le but est de virer les valeurs extremes (souvent erronnees) pour avoir un rectangle solide
def meilleur_rect((x1,y1,x2,y2)) :
    
    x1.sort()
    print x1
    best_x1 = x1[15] #15 correspond ~ a 1% d'erreur.
    y1.sort()
    best_y1 = y1[15]
    x2.sort()
    best_x2 = x2[len(x2)-15]
    y2.sort()
    best_y2 = y2[len(y2)-15]
    print '('+str(best_x1)+','+str(best_y1)+') -> ('+str(best_x2)+','+str(best_y2)+')'

    return (best_x1, best_y1, best_x2, best_y2)


meilleur_rect(rectangle_bouche())

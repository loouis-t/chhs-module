#Créé le 03/08/2020, par Louis Travaux

import os, shutil, ctypes, random, getpass #os et shutil pour le contrôle et la modification des fichiers et dossiers, ctypes pour changer le fd, random pour le choix aléatoire du fd
from PIL import Image, ImageChops   #PIL pour le tri des images

class chhs():
    def __init__(self):
        #definition du chemin d'accès au dossier où windows stocke les images "windows à la une"
        self.win_une_path = "C:\\Users\\{}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets".format(getpass.getuser())
        #definition du chemin d'accès au dossier dans lequel on stocke les images traitées
        self.mypath = str(os.path.realpath("win_a_la_une"))

        #copier fichiers depuis le dossier source vers le dossier de destination
        liste_images_source = os.listdir(self.win_une_path)
        for img in liste_images_source:
            shutil.copy("{}\\{}".format(self.win_une_path, img), self.mypath)

        #renomer les images en .jpg et supprimer les doublons
        liste_fichiers_recuperees = os.listdir(self.mypath)
        for name in liste_fichiers_recuperees:
            #définition de l'ancien nom et du nouveau (chemin d'accès/path compris dans le nom)
            ancien_path = self.mypath + "\\" + name
            nouveau_path = self.mypath + "\\" + name + ".jpg"

            if os.path.exists(nouveau_path) == False and name.count('.jpg') < 1:    #renommer en .jpg
                os.rename(ancien_path, nouveau_path)
            elif os.path.exists(nouveau_path) == True:      #supprimer les doublons
                os.remove(ancien_path)
            
        
        #supprimer images dont définition différente de 1920x1080
        liste_images_recuperees = os.listdir(self.mypath)
        for image in liste_images_recuperees:
            path_image = self.mypath + "\\" + image
            with Image.open(path_image) as m:
                dimension = m.size
                m.close()
                if dimension[0] != 1920 and dimension[1] != 1080:
                    os.remove(path_image)

        #supprimer doublons
        images = os.listdir(self.mypath)
        for im1 in images: #on compare les images entre elles
            for im2 in images: #obligés de créer deux fois une variable 'pour chaque image de la liste' pour pouvoir comparer
                if im1 != im2: #inutile de comparer une image avec elle meme
                    path_im1 = self.mypath + "\\" + im1 #ajouter le chemin d'accès au nom de l'image1
                    path_im2 = self.mypath + "\\" + im2 #ajouter le chemin d'accès au nom de l'image2
                    try:    #comparer
                        with Image.open(path_im1) as n:
                            try:
                                with Image.open(path_im2) as o:
                                    comparaison = ImageChops.difference(n, o)
                                    n.close()
                                    m.close()
                                    resultat = comparaison.getbbox()
                                    if resultat == None:    #si les images n'ont pas de différence, on en supprime une
                                        os.remove(path_im1)
                                        print(im1 + "->Supprimée")
                            except:
                                pass
                    except:
                        pass

        #changer noms aléatoires de windows en "fond_ecran_n" en prenant un n superieur a celui deja existant
        liste_finale = os.listdir(self.mypath)
        rang = [0]
        for name in liste_finale:
            try:    #try/except : prendre en compte nvx fd  
                numero = int((name.split(".jpg")[0]).split("fond_ecran_")[1]) #recuperer n de chaque fd
                rang.append(numero) #ajouter ces n dans une liste 
            except:
                pass
        
        n = max(rang) + 1  #recuperer le plus grand n et ajouter 1
        for fd in liste_finale:
            if fd.count("fond_ecran_") < 1:
                ancien_nom = self.mypath + "\\" + fd
                nouveau_nom = self.mypath + "\\" + "fond_ecran_" + str(n) + ".jpg"
                os.rename(ancien_nom, nouveau_nom)
                n += 1
        
        print("liste images: {}".format(os.listdir(self.mypath)))
        print("(id: 0-n)")

    def aleatoire(self):
        liste_fd = os.listdir(self.mypath)
        N = random.choice(liste_fd)     #choisir aléatoirement dans liste images dossier
        path_N = self.mypath + "\\" + N     #ajouter chemin d'accès/path au nom de l'image
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path_N, 0)    #mettre en fond d'écran

    def id(self, id):
        liste_fd = os.listdir(self.mypath)
        try:
            numero = self.mypath + "\\" + liste_fd[id]      #ajouter chemin d'accès/path au nom de l'image
            ctypes.windll.user32.SystemParametersInfoW(20, 0, numero, 0)    #mettre en fond d'écran
        except:
            print('list index out of range')    #gérer l'erreur: l'id indiqué à l'appel de la fonction dépasse la longueur de la liste
        

chhs = chhs()

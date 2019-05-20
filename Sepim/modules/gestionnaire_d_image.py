# coding=utf-8

"""
    Module qui permet de centraliser/gérer les images traitées
"""

# =================================================================================================
# PARAMETRES GLOBAUX
# =================================================================================================

__author__ = 'Julien LEPAIN'
__email__ = 'julien.lepain.31@gmail.com'
__version__ = '1.0'
__maintainer__ = 'Julien LEPAIN'
__date__ = '16/05/2019'
__status = 'dev'

# ==================================================================================================
# IMPORTS
# ==================================================================================================

import os
from PIL import Image
from Sepim.modules.objet_image import ObjetImage
import numpy

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ===============================
class GestionnaireDImage(object):
    """
        Classe qui permet des gérer une image à traiter

        :ivar __nom_de_l_image_a_traiter: nom de l'image à traiter
        :type __nom_de_l_image_a_traiter: str

        :ivar __dossier_contenant_les_images_a_traiter: nom du dossier contenant les images à traiter
        :type __dossier_contenant_les_images_a_traiter: str

        :ivar __couleur_de_separation: couleur de séparation entre les sous-images d'une image
        :type __couleur_de_separation: numpy.ndarray

        :ivar __dossier_de_sauvegarde_des_sous_images: dossier de sauvegarde des sous-images générées
        :type __dossier_de_sauvegarde_des_sous_images: str

        :ivar __liste_des_sous_images: liste des images créées
        :type __liste_des_sous_images: list[ObjetImage]

        :ivar __image_chargee: données de l'image chargée
        :type __image_chargee: numpy.ndarray

        :ivar __hauteur_image_chargee: hauteur de l'image chargée
        :type __hauteur_image_chargee: long

        :ivar __largeur_image_chargee: largeur de l'image chargée
        :type __largeur_image_chargee: long
    """

    # ==========================================================================================================
    def __init__(self, nom_de_l_image_a_traiter, dossier_contenant_les_images_a_traiter, couleur_de_separation):
        """
            Constructeur de la classe

            :param nom_de_l_image_a_traiter: nom de l'image à traiter
            :type nom_de_l_image_a_traiter: str

            :param dossier_contenant_les_images_a_traiter: nom du dossier contenant les images à traiter
            :type dossier_contenant_les_images_a_traiter: str

            :param couleur_de_separation: couleur de séparation entre les sous-images d'une image
            :type couleur_de_separation: numpy.ndarray
        """

        # Attributs d'instance initialisés via les paramètres du constructeur
        self.__nom_de_l_image_a_traiter = nom_de_l_image_a_traiter
        self.__dossier_contenant_les_images_a_traiter = dossier_contenant_les_images_a_traiter
        self.__couleur_de_separation = couleur_de_separation

        # Autres attributs d'instance
        self.__dossier_de_sauvegarde_des_sous_images = os.path.join(os.path.abspath(dossier_contenant_les_images_a_traiter), "Sauvegarde")
        self.__liste_des_sous_images = []
        self.__image_chargee = None
        self.__hauteur_image_chargee = 0
        self.__largeur_image_chargee = 0

    # =================================================================================================
    def ajouter_une_sous_image(self, limite_haute, limite_gauche, limite_basse = 0, limite_droite = 0):
        """
            Méthode qui permet d'ajouter une sous-image à la liste des sous-images

            :param limite_haute: limite haute de l'image à créer
            :type limite_haute: long

            :param limite_gauche: limite gauche de l'image à créer
            :type limite_gauche: long

            :param limite_basse: limite basse de l'image à créer
            :type limite_basse: long

            :param limite_droite: limite droite de l'image à créer
            :type limite_droite: long
        """

        # création d'un nouvel objet ObjetImage (i.e. une nouvelle sous-image)
        try:

            sous_image = ObjetImage(limite_haute, limite_gauche, limite_basse, limite_droite)

        except Exception:

            sous_image = None
            # message

        # ajout de la nouvelle sous-image à la liste des sous-images
        try:

            self.__liste_des_sous_images.append(sous_image)

        except Exception:

            pass
            # message

    # ========================================
    def chargement_de_l_image_a_traiter(self):
        """
            Méthode qui permet de charger l'image à traiter et de la convertir si nécessaire
        """

        # Récupération du dossier courant
        dossier_avant_deplacement = os.getcwd()

        # Déplacement dans le dossier qui contient les images à traiter
        try:

            os.chdir(self.__dossier_contenant_les_images_a_traiter)

        except Exception:

            pass
            # gérer l'exception si le dossier n'existe pas

        # Chargement de l'image
        try:

            self.__image_chargee = numpy.array(Image.open(self.__nom_de_l_image_a_traiter))

        except Exception:

            self.__image_chargee = None
            # message

        # Retour dans le dossier courant
        os.chdir(dossier_avant_deplacement)

        # Conversion, si nécessaire, des données de l'image : on transforme les float (allant de 0 à 1) en entiers (allant de 0 à 255)
        if self.__image_chargee.dtype == numpy.float32:

            self.__image_chargee = (self.__image_chargee * 255).astype(numpy.uint8)

    # ========================================
    def calcul_dimensions_image_chargee(self):
        """
            Méthode qui permet de calculer les dimensiosn de l'image chargée
        """

        try:

            self.__hauteur_image_chargee = len(self.__image_chargee)

        except Exception:

            self.__hauteur_image_chargee = None

        try:

            self.__largeur_image_chargee = len(self.__image_chargee[0])

        except Exception:

            self.__largeur_image_chargee = None

    # ===================================
    def extraction_des_sous_images(self):
        """
            Méthode qui permet d'extraire, d'une image chargée, ses sous-images
        """

        # initialisation de la condition d'arrêt de l'extraction
        extraction_terminee = False

        # boucle d'extraction
        while not extraction_terminee:

            # initialisation de la condition de sortie sur la hauteur
            condition_de_sortie_sur_la_hauteur = False

            # itération sur la hauteur de l'image
            for hauteur_actuelle in range(self.__hauteur_image_chargee):

                # vérification de la condition de sortie sur la hauteur
                if condition_de_sortie_sur_la_hauteur:

                    break

                # itération sur la largeur de l'image
                for largeur_actuelle in range(self.__largeur_image_chargee):

                    # le pixel courant ne se situe pas sur un séparateur
                    if not numpy.array_equal(self.__image_chargee[hauteur_actuelle, largeur_actuelle], self.__couleur_de_separation):

                        # ajout d'une nouvelle sous-image
                        self.ajouter_une_sous_image(hauteur_actuelle, largeur_actuelle)

                        # récupération de la dernière sous-image ajoutée
                        sous_image_actuelle = self.__liste_des_sous_images[-1]

                        # itération sur la largeur de la hauteur actuelle afin de déterminer la limite droite de l'image
                        for largeur in range(largeur_actuelle, self.__largeur_image_chargee):

                            if (numpy.array_equal(self.__image_chargee[hauteur_actuelle, largeur], self.__couleur_de_separation)) or (largeur == (self.__largeur_image_chargee - 1)):

                                if largeur == (self.__largeur_image_chargee - 1):

                                    sous_image_actuelle.set_limite_droite(largeur)

                                else:

                                    sous_image_actuelle.set_limite_droite(largeur - 1)

                                break

                        # itération sur la hauteur de la largeur actuelle afin de déterminer la limite basse de l'image
                        for hauteur in range(hauteur_actuelle, self.__hauteur_image_chargee):

                            if (numpy.array_equal(self.__image_chargee[hauteur, largeur_actuelle], self.__couleur_de_separation)) or (hauteur == (self.__hauteur_image_chargee - 1)):

                                if hauteur == (self.__hauteur_image_chargee - 1):

                                    sous_image_actuelle.set_limite_basse(hauteur)

                                else:

                                    sous_image_actuelle.set_limite_basse(hauteur - 1)

                                break

                        # définit les données de la sous-image actuelle
                        sous_image_actuelle.set_donnees_image(self.__image_chargee)

                        # récupération des limites de la sous-image actuelle
                        lim_h = sous_image_actuelle.get_limite_haute()
                        lim_b = sous_image_actuelle.get_limite_basse()
                        lim_g = sous_image_actuelle.get_limite_gauche()
                        lim_d = sous_image_actuelle.get_limite_droite()

                        # modification de l'image chargée :
                        # remplacement des données de la sous-image par la couleur de séparation
                        self.__image_chargee[lim_h:lim_b + 1, lim_g:lim_d + 1] = self.__couleur_de_separation

                        # ré-initilisation de la condition de sortie sur la hauteur
                        condition_de_sortie_sur_la_hauteur = True
                        break

            # vérification de la fin d'extraction :
            # si tous les éléments de l'image chargée correspondent à la couleur de séparation alors l'extraction se termine
            if (self.__image_chargee == self.__couleur_de_separation).all():

                extraction_terminee = True

    # ===================================
    def sauvegarde_des_sous_images(self):
        """
            Méthode qui permet de sauvegarder les sous-iamges générées à partir de l'image
        """

        # itération sur les sous-image de l'image chargée
        for indice, image in enumerate(self.__liste_des_sous_images):

            # définition du nom du fichier de la sous-image courante
            nom_de_l_image = self.__nom_de_l_image_a_traiter.split(".")[0]
            extension_de_l_image = self.__nom_de_l_image_a_traiter.split(".")[1]
            nom_du_fichier_a_enregistrer = "{}_{}{}.{}".format(nom_de_l_image, 0 if indice < 10 else "", indice, extension_de_l_image)
            nom_absolu_du_fichier_a_enregistrer = os.path.join(self.__dossier_de_sauvegarde_des_sous_images, nom_du_fichier_a_enregistrer)

            # création du dossier de sauvegarde s'il n'existe pas déjà
            try:

                os.makedirs(self.__dossier_de_sauvegarde_des_sous_images)

            except FileExistsError:

                pass

            # sauvegarde de l'image
            image_a_enregistrer = Image.fromarray(image.get_donnees_image())
            image_a_enregistrer.save(nom_absolu_du_fichier_a_enregistrer)

# ==================================================================================================
# FONCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

# coding=utf-8

"""
    Module qui permet de gérer la rotation de sous-images en provenance d'une image

    https://www.pyimagesearch.com/2015/02/09/removing-contours-image-using-python-opencv/         ==> à tester ?
"""

# =================================================================================================
# PARAMETRES GLOBAUX
# =================================================================================================

__author__ = 'Julien LEPAIN'
__email__ = 'julien.lepain.31@gmail.com'
__version__ = '1.0'
__maintainer__ = 'Julien LEPAIN'
__date__ = '05/06/2019'
__status = 'dev'

# ==================================================================================================
# IMPORTS
# ==================================================================================================

from numpy import array_equal, where, cos, sin, median
from cv2 import cvtColor, Canny, HoughLines, COLOR_RGB2GRAY
from math import pi, degrees, atan2
from scipy import ndimage

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ==============================
class RotationDesImages(object):
    """
        Classe de rotation d'une image

        :ivar __image: image à faire tourner
        :type __image: Sepim.modules.objet_image.ObjetImage

        :ivar __couleur_de_separation: couleur de séparation entre les sous-images d'une image
        :type __couleur_de_separation: numpy.ndarray
    """

    # ===============================================
    def __init__(self, image, couleur_de_separation):
        """
            Constructeur de la classe

            :param image: image à faire tourner
            :type image: Sepim.modules.objet_image.ObjetImage

            :param couleur_de_separation: couleur de séparation entre les sous-images d'une image
            :type couleur_de_separation: numpy.ndarray
        """

        # Attributs d'instance initialisés via les paramètres du constructeur
        self.__image = image
        self.__couleur_de_separation = couleur_de_separation

        # Autres attributs d'instance
        # N/A

    # ===========================
    def detection_rotation(self):
        """
            Méthode qui permet de détectter si une image nécessite une rotation et de lancer la rotation si elle en a besoin

            TODO: à améliorer, ne fonctionne pas terrible...
        """

        # initialisations
        rotation = False        # paramètre de rotation (initialisé à False)
        donnees_image = self.__image.get_donnees_image()
        largeur = 0

        # itération sur la hauteur de l'image
        for hauteur in reversed(range(donnees_image.shape[0])):

            # si un pixel ne se trouve pas sur la séparation le paramètre de rotation passe à True
            if not array_equal(donnees_image[hauteur, largeur], self.__couleur_de_separation):

                rotation = True
                break

        # si le paramètre de rotation est à True on lance la rotation de l'image
        if rotation:

            self.rotation_image()

    # =======================
    def rotation_image(self):
        """
            Méthode qui permet de faire tourner une image
        """

        # Récupération des données de l'image à traiter
        donnees_image = self.__image.get_donnees_image()

        # On modifie les pixels qui ont la même couleur que la séparation : on définit leur nouvelle couleur comme étant le noir
        donnees_image[where((donnees_image == [181, 230, 29]).all(axis = 2))] = [0, 0, 0]

        # Conversion des données de l'image en nuances de gris
        donnees_image_nuances_de_gris = cvtColor(donnees_image, COLOR_RGB2GRAY)

        # Appel à la méthode Canny afin de détecter les bords de l'image
        bords_de_l_image = Canny(donnees_image_nuances_de_gris, 100, 100, apertureSize = 3)

        # Appel à la méthode HoughLines afin de détecter les lignes principales de l'image
        lignes_principales_de_l_image = HoughLines(bords_de_l_image, 1, pi / 180.0, 100)

        # Calcul de l'angle de rotation de l'image en utilisant la première ligne principale de l'image
        angles = []

        for rho, theta in lignes_principales_de_l_image[0]:

            a = cos(theta)
            b = sin(theta)

            x0 = a * rho
            y0 = b * rho

            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)

            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * a)

            angle = degrees(atan2(y2 - y1, x2 - x1))
            angles.append(angle)

        angle_median = median(angles)

        # Rotation de l'image
        donnees_image_tournee = ndimage.rotate(donnees_image, angle_median)

        # Appel à la méthode Canny afin de détecter les bords de l'image tournée
        bords_de_l_image_tournee = Canny(donnees_image_tournee, 100, 100, apertureSize = 3)

        # Calcul des nouvelles limites de l'image tournée
        largeur_point_A, hauteur_point_A, largeur_point_B, hauteur_point_B = self.calcul_nouvelles_limites_image_tournee(bords_de_l_image_tournee)

        # Redéfinition des limites de l'image à traiter
        self.__image.set_limite_droite(largeur_point_B)
        self.__image.set_limite_basse(hauteur_point_B)
        self.__image.set_limite_gauche(largeur_point_A)
        self.__image.set_limite_haute(hauteur_point_A)

        # Redéfinition des données de l'image à traiter
        self.__image.set_donnees_image(donnees_image_tournee)

    # ===================================================================
    def calcul_nouvelles_limites_image_tournee(self, donnees_de_l_image):
        """
            Méthode qui permet de calculer les nouvelles limites d'une image qui a été tournée
            Les limites retournées sont les largeur et hauteur de deux points : les points A et B
            Le point A correspond au bord haut, gauche de l'image
            Le point B correspond au bord bas, droit de l'image

            :param donnees_de_l_image: données de l'image
            :type donnees_de_l_image: numpy.ndarray

            :return: les positions (en largeur et hauteur) des points A et B
            :rtype: tuple(int, int, int ,int)
        """

        # initialisation de la condition d'arrêt de l'extraction
        extraction_terminee = False

        # boucle d'extraction
        while not extraction_terminee:

            # initialisation de la condition de sortie sur la hauteur
            condition_de_sortie_sur_la_hauteur = False

            # itération sur la hauteur de l'image
            for hauteur_actuelle in range(donnees_de_l_image.shape[0]):

                # vérification de la condition de sortie sur la hauteur
                if condition_de_sortie_sur_la_hauteur:

                    break

                # itération sur la largeur de l'image
                for largeur_actuelle in range(donnees_de_l_image.shape[1]):

                    # le pixel courant n'est pas noir
                    if donnees_de_l_image[hauteur_actuelle, largeur_actuelle] != 0:

                        largeur_point_A = largeur_actuelle
                        hauteur_point_A = hauteur_actuelle

                        condition_de_sortie_sur_la_hauteur = True
                        extraction_terminee = True
                        break

        # initialisation de la condition d'arrêt de l'extraction
        extraction_terminee = False

        # boucle d'extraction
        while not extraction_terminee:

            # initialisation de la condition de sortie sur la hauteur
            condition_de_sortie_sur_la_hauteur = False

            # itération sur la hauteur de l'image
            for hauteur_actuelle in reversed(range(donnees_de_l_image.shape[0])):

                # vérification de la condition de sortie sur la hauteur
                if condition_de_sortie_sur_la_hauteur:
                    break

                # itération sur la largeur de l'image
                for largeur_actuelle in reversed(range(donnees_de_l_image.shape[1])):

                    # le pixel courant n'est pas noir
                    if donnees_de_l_image[hauteur_actuelle, largeur_actuelle] != 0:

                        largeur_point_B = largeur_actuelle
                        hauteur_point_B = hauteur_actuelle

                        condition_de_sortie_sur_la_hauteur = True
                        extraction_terminee = True
                        break

        return largeur_point_A, hauteur_point_A, largeur_point_B, hauteur_point_B

# ==================================================================================================
# FONCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

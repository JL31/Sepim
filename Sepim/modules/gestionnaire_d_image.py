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

from Sepim.modules.objet_image import ObjetImage
from Sepim.modules.gestionnaire_rotation_des_images import RotationDesImages

import os
import sys
from numpy import float32, uint8, array_equal
from cv2 import imread, cvtColor, COLOR_BGR2RGB, imwrite, COLOR_RGB2BGR

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

sys.setrecursionlimit(2000)

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
        self.__sous_image_actuelle = None

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

            image = imread(self.__nom_de_l_image_a_traiter)
            self.__image_chargee = cvtColor(image, COLOR_BGR2RGB)

        except Exception:

            self.__image_chargee = None
            # message

        # Retour dans le dossier courant
        os.chdir(dossier_avant_deplacement)

        # Conversion, si nécessaire, des données de l'image : on transforme les float (allant de 0 à 1) en entiers (allant de 0 à 255)
        if self.__image_chargee.dtype == float32:

            self.__image_chargee = (self.__image_chargee * 255).astype(uint8)

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

                    # le pixel courant ne se situe pas sur le séparateur
                    if not array_equal(self.__image_chargee[hauteur_actuelle, largeur_actuelle], self.__couleur_de_separation):

                        # ajout d'une nouvelle sous-image
                        self.ajouter_une_sous_image(hauteur_actuelle, largeur_actuelle)

                        # récupération de la dernière sous-image ajoutée
                        self.__sous_image_actuelle = self.__liste_des_sous_images[-1]

                        # calcul des limites basse et droite de la sous-image actuelle
                        largeur_finale, hauteur_finale, _ = self.calcul_limites_basse_et_droite(hauteur_actuelle, largeur_actuelle, True)

                        # affectation des valeurs des limites basses et droites à la sous-image actuelle
                        self.affectation_des_limites_basse_et_droite(hauteur_finale, largeur_finale)

                        # défini les données de la sous-image actuelle
                        self.__sous_image_actuelle.set_donnees_image(self.__image_chargee)

                        # récupération des limites de la sous-image actuelle
                        lim_h = self.__sous_image_actuelle.get_limite_haute()
                        lim_g = self.__sous_image_actuelle.get_limite_gauche()

                        lim_b = self.__sous_image_actuelle.get_limite_basse()
                        lim_d = self.__sous_image_actuelle.get_limite_droite()

                        # modification de l'image chargée :
                        # remplacement des données de la sous-image par la couleur de séparation
                        self.__image_chargee[lim_h:lim_b + 1, lim_g:lim_d + 1] = self.__couleur_de_separation

                        # ré-initilisation de la condition de sortie sur la hauteur
                        condition_de_sortie_sur_la_hauteur = True
                        break

            # vérification de la fin d'extraction :
            # si tous les éléments de l'image chargée correspondent à la couleur de séparation alors l'extraction est terminée
            if (self.__image_chargee == self.__couleur_de_separation).all():

                extraction_terminee = True

    # ==================================================================
    def affectation_des_limites_basse_et_droite(self, hauteur, largeur):
        """
            Méthode qui permet d'affecter les limites basses et droites à la sous-image actuelle

            :param hauteur: nouvlele valeur de la limite basse (seulement si strictement supérieure à la valeur actuelle)
            :type hauteur: long

            :param largeur: nouvelle valeur de la limite droite (seulement si strictement supérieure à la valeur actuelle)
            :type largeur: long
        """

        if hauteur > self.__sous_image_actuelle.get_limite_basse():

            self.__sous_image_actuelle.set_limite_basse(hauteur)

        if largeur > self.__sous_image_actuelle.get_limite_droite():

            self.__sous_image_actuelle.set_limite_droite(largeur)

    # =========================================================================================
    def analyse_existence_pixel_sur_separation(self, position_verticale, position_horizontale):
        """
            Méthode qui permet de vérifier s'il existe un pixel sur la séparation pour les coordonnées indiquées en argument

            :param position_verticale: position verticale
            :type position_verticale: long

            :param position_horizontale: position horizontale
            :type position_horizontale: long

            :return: résultat de de l'analyse :
                                                - si un pixel a été trouvé et que la position horizontale est supérieure à la limite gauche de la sous-image actuelle on renvoie True
                                                - sinon on renvoie False
            :rtype: bool
        """

        # itération depuis la position horizontale passée en argument et le nord gauche de l'image chargée
        for pos_hor in reversed(range(position_horizontale)):

            # on ne se situe pas sur la séparation
            if not array_equal(self.__image_chargee[position_verticale, pos_hor], self.__couleur_de_separation):

                # la position horizontale actuelle est supérieure à la limite gauche de la sous-image actuelle : on renvoie True
                if pos_hor >= self.__sous_image_actuelle.get_limite_gauche():

                    return True

                # sinon on renvoie False
                else:

                    return False

        return False

    # ==========================================================================================================
    def calcul_position_horizontale_demarrage(self, position_verticale_actuelle, position_horizontale_actuelle):
        """
            Méthode qui permet de calculer la position horizontale pour le démarrage du calcul des limites basse et droite de la sous-image actuelle

            :param position_verticale_actuelle: position verticale actuelle (en pixel)
            :type position_verticale_actuelle: long

            :param position_horizontale_actuelle: position horizontale actuelle (en pixel)
            :type position_horizontale_actuelle: long

            :return: la position horizontale de démarrage
            :rtype: long
        """

        # initialisation de la condition de sortie
        # ----------------------------------------

        sortie = False

        # itération tant que la condition de sortie n'est pas vraie
        # ---------------------------------------------------------

        while not sortie:

            if position_horizontale_actuelle == 0:

                position_horizontale_actuelle -= 1
                sortie = True

            elif array_equal(self.__image_chargee[position_verticale_actuelle, position_horizontale_actuelle], self.__couleur_de_separation):

                sortie = True

            else:

                position_horizontale_actuelle -= 1

        # mise-à-jour, si nécessaire, de la limite gauche de la sous-image actuelle
        # -------------------------------------------------------------------------

        if position_horizontale_actuelle < self.__sous_image_actuelle.get_limite_gauche():

            self.__sous_image_actuelle.set_limite_gauche(position_horizontale_actuelle + 1)


        # retour de la méthode
        # --------------------

        return position_horizontale_actuelle + 1

    # =====================================================================================================================================================
    def calcul_limites_basse_et_droite(self, position_verticale_actuelle, position_horizontale_actuelle, initialisation_position_horizontale_de_demarrage):
        """
            Méthode qui permet de calculer les valeurs des limites basses et droites de la sous-image actuelle.
            Ce calcul sera itératif.

            :param position_verticale_actuelle: position verticale actuelle (en pixel)
            :type position_verticale_actuelle: long

            :param position_horizontale_actuelle: position horizontale actuelle (en pixel)
            :type position_horizontale_actuelle: long

            :param initialisation_position_horizontale_de_demarrage: si ce paramètre est à :
            - True : il faut utiliser la méthode "calcul_position_horizontale_demarrage" afin de déterminer la position horizontale à partir de laquelle le calcul démarre
            - False: la position horizontale à partir de laquelle le calcul débute est celle passée en argument de cette méthode
            :type initialisation_position_horizontale_de_demarrage: bool

            :return: les valeurs des limites droite et basse ainsi que de l'indicateur de fin de calcul
            :rtype: tuple(long, long, bool)
        """

        # initialisations
        # ---------------

        largeur_maximale = False
        fin_du_calcul = False       # indicateur de fin de calcul : cette variable permet de savoir si le calcul des limites est terminé ou non

        pos_hor_actuelle = position_horizontale_actuelle
        pos_vert_actuelle = position_verticale_actuelle


        # calcul de la position horizontale de démarrage
        # ----------------------------------------------

        # si le paramètre d'initialisation de la position horizontale de démarrage est à True on le passe à False
        if initialisation_position_horizontale_de_demarrage:

            initialisation_position_horizontale_de_demarrage = False

        # sinon on calcule la position horizontale de démarrage du calcul
        else:

            pos_hor_actuelle = self.calcul_position_horizontale_demarrage(pos_vert_actuelle, pos_hor_actuelle)


        # itération sur la largeur
        # ------------------------

        while not largeur_maximale:

            # on se trouve sur le bord droit de l'image chargée
            if pos_hor_actuelle == (self.__largeur_image_chargee - 1):

                # on ne se trouve pas sur le bord bas de l'image chargée
                if pos_vert_actuelle != (self.__hauteur_image_chargee - 1):

                    # Les pixels :
                    # - situé à la même position horizontale mais sur la la ligne suivante
                    # - situé un pixel plus à gauche sur la ligne suivante
                    # sont situés sur la séparation
                    if (array_equal(self.__image_chargee[pos_vert_actuelle + 1, pos_hor_actuelle], self.__couleur_de_separation)) and \
                       (array_equal(self.__image_chargee[pos_vert_actuelle + 1, pos_hor_actuelle - 1], self.__couleur_de_separation)):

                        largeur_finale = pos_hor_actuelle
                        hauteur_finale = pos_vert_actuelle

                        largeur_maximale = True
                        fin_du_calcul = True

                    # s'ils ne sont pas sur la séparation
                    else:

                        # on commence par mettre-à-jour les valeurs des limites basse et droite de la sous-image actuelle
                        self.affectation_des_limites_basse_et_droite(pos_vert_actuelle, pos_hor_actuelle - 1)

                        # on fait appel une nouvelle fois à la méthode de calcul des limites basse et droite en mettant à jour les positions horizontale et et verticale :
                        # on se place sur la ligne suivante et un pixel plus à gauche que la position actuelle
                        largeur_finale, hauteur_finale, fin_du_calcul = self.calcul_limites_basse_et_droite(pos_vert_actuelle + 1, pos_hor_actuelle - 1, initialisation_position_horizontale_de_demarrage)

                # on se trouve sur le bord bas de l'image chargée
                else:

                    largeur_finale = pos_hor_actuelle
                    hauteur_finale = pos_vert_actuelle

                    largeur_maximale = True
                    fin_du_calcul = True

            # on se trouve sur le bord bas de l'image chargée
            elif pos_vert_actuelle == (self.__hauteur_image_chargee - 1):

                # on ne se trouve pas sur le bord droit de l'image chargée
                if pos_hor_actuelle != (self.__largeur_image_chargee - 1):

                    # Les pixels :
                    # - situé à la même position horizontale mais sur la ligne précédente
                    # - courant
                    # sont situés sur la séparation
                    if (array_equal(self.__image_chargee[pos_vert_actuelle - 1, pos_hor_actuelle], self.__couleur_de_separation)) and \
                       (array_equal(self.__image_chargee[pos_vert_actuelle, pos_hor_actuelle], self.__couleur_de_separation)):

                        largeur_finale = pos_hor_actuelle - 1
                        hauteur_finale = pos_vert_actuelle

                        largeur_maximale = True
                        fin_du_calcul = True

                # s'ils ne sont pas sur la séparation
                else:

                    largeur_finale = pos_hor_actuelle
                    hauteur_finale = pos_vert_actuelle

                    largeur_maximale = True
                    fin_du_calcul = True

            # on ne se trouve ni sur le bord droit ni sur le bord bas de l'image chargée
            elif array_equal(self.__image_chargee[pos_vert_actuelle, pos_hor_actuelle], self.__couleur_de_separation):

                # si :
                # - on ne se situe pas sur le bord bas de l'image chargée
                # - on ne se situe pas sur le bord gauche de l'image chargée
                # - les pixels :
                #   + situé à la même position horizontale mais sur la la ligne suivante
                #   + situé un pixel plus à gauche sur la ligne suivante
                #   sont situés sur la séparation
                if (pos_vert_actuelle != (self.__hauteur_image_chargee - 1)) and \
                   (pos_hor_actuelle != 0) and \
                   (array_equal(self.__image_chargee[pos_vert_actuelle + 1, pos_hor_actuelle], self.__couleur_de_separation)) and \
                   (array_equal(self.__image_chargee[pos_vert_actuelle + 1, pos_hor_actuelle - 1], self.__couleur_de_separation)):

                    # il existe, sur la ligne suivante, un pixel qui n'est pas sur la séparation
                    if self.analyse_existence_pixel_sur_separation(pos_vert_actuelle + 1, pos_hor_actuelle - 2):

                        # on commence par mettre-à-jour les valeurs des limites basse et droite de la sous-image actuelle
                        self.affectation_des_limites_basse_et_droite(pos_vert_actuelle, pos_hor_actuelle - 1)

                        # on fait appel une nouvelle fois à la méthode de calcul des limites basse et droite en mettant à jour les positions horizontale et et verticale :
                        # on se place sur la ligne suivante et deux pixels plus à gauche que la position actuelle
                        largeur_finale, hauteur_finale, fin_du_calcul = self.calcul_limites_basse_et_droite(pos_vert_actuelle + 1, pos_hor_actuelle - 2, initialisation_position_horizontale_de_demarrage)

                    # sinon
                    else:

                        largeur_finale = pos_hor_actuelle - 1
                        hauteur_finale = pos_vert_actuelle

                        largeur_maximale = True
                        fin_du_calcul = True

                # sinon
                else:

                    # on ne se situe pas sur le bord bas de l'image chargée
                    if pos_vert_actuelle != (self.__hauteur_image_chargee - 1):

                        # on commence par mettre-à-jour les valeurs des limites basse et droite de la sous-image actuelle
                        self.affectation_des_limites_basse_et_droite(pos_vert_actuelle, pos_hor_actuelle - 1)

                        # on fait appel une nouvelle fois à la méthode de calcul des limites basse et droite en mettant à jour les positions horizontale et et verticale :
                        # on se place sur la ligne suivante et un pixel plus à gauche que la position actuelle
                        largeur_finale, hauteur_finale, fin_du_calcul = self.calcul_limites_basse_et_droite(pos_vert_actuelle + 1, pos_hor_actuelle - 1, initialisation_position_horizontale_de_demarrage)


            # vérification de la fin du calcul
            # --------------------------------

            # le calcul des limites est terminé : on passe le paramètre "largeur_maximale" à True pour sortir de la boucle d'itération sur la largeur
            if fin_du_calcul:

                largeur_maximale = True

            # sinon on continue d'itérer sur la largeur
            else:

                pos_hor_actuelle += 1


        # retour de la méthode
        # --------------------

        return largeur_finale, hauteur_finale, fin_du_calcul

    # =================================
    def rotation_des_sous_images(self):
        """
            Méthode qui permet de gérer la rotation des sous-images
        """

        # itération sur les sous-image de l'image chargée
        for indice, image in enumerate(self.__liste_des_sous_images):

            # création d'ine instance de rotation des images
            instance_rot_img = RotationDesImages(image, self.__couleur_de_separation)

            # lancement de la détection de la rotation d'une image
            instance_rot_img.detection_rotation()

    # ===================================
    def sauvegarde_des_sous_images(self):
        """
            Méthode qui permet de sauvegarder les sous-images générées à partir de l'image
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
            imwrite(nom_absolu_du_fichier_a_enregistrer, cvtColor(image.get_donnees_image(), COLOR_RGB2BGR))

# ==================================================================================================
# FONCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

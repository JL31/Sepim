# coding=utf-8

"""
    Module qui permet de créer une image (ou sous-image)
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

import matplotlib.pyplot as plt

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# =======================
class ObjetImage(object):
    """
        Classe de création d'une nouvelle image

        :ivar __limite_haute: limite haute de l'image
        :type __limite_haute: long

        :ivar __limite_gauche: limite gauche de l'image
        :type __limite_gauche: long

        :ivar __limite_basse: limite basse de l'image
        :type __limite_basse: long

        :ivar __limite_droite: limite droite de l'image
        :type __limite_droite: long

        :ivar __donnees_image: les données de l'image
        :type __donnees_image: None | numpy.ndarray
    """

    # ===========================================================================
    def __init__(self, limite_haute, limite_gauche, limite_basse, limite_droite):
        """
            Constructeur de la classe

            :param limite_haute: limite haute de l'image
            :type limite_haute: long

            :param limite_gauche: limite gauche de l'image
            :type limite_gauche: long

            :param limite_basse: limite basse de l'image
            :type limite_basse: long

            :param limite_droite: limite droite de l'image
            :type limite_droite: long
        """

        self.__limite_haute = limite_haute
        self.__limite_gauche = limite_gauche
        self.__limite_basse = limite_basse
        self.__limite_droite = limite_droite
        self.__donnees_image = None

    # =========================
    def get_limite_haute(self):
        """
            Accesseur de l'attribut __limite_haute

            :return: __limite_haute
            :rtype: long
        """

        return self.__limite_haute

    # ==========================
    def get_limite_gauche(self):
        """
            Accesseur de l'attribut __limite_gauche

            :return: __limite_gauche
            :rtype: long
        """

        return self.__limite_gauche

    # =========================
    def get_limite_basse(self):
        """
            Accesseur de l'attribut __limite_basse

            :return: __limite_basse
            :rtype: long
        """

        return self.__limite_basse

    # ==========================
    def get_limite_droite(self):
        """
            Accesseur de l'attribut __limite_droite

            :return: __limite_droite
            :rtype: long
        """

        return self.__limite_droite

    # ==========================
    def get_donnees_image(self):
        """
           Accesseur de l'attribut __donnees_image
        """

        return self.__donnees_image

    # =================================
    def set_limite_haute(self, valeur):
        """
            Mutateur de l'attribut __limite_haute

            :param valeur: nouvelle valeur pour l'attribut __limite_haute
            :type valeur: long
        """

        self.__limite_haute = valeur

    # ==================================
    def set_limite_gauche(self, valeur):
        """
            Mutateur de l'attribut __limite_gauche

            :param valeur: nouvelle valeur pour l'attribut __limite_gauche
            :type valeur: long
        """

        self.__limite_gauche = valeur

    # =================================
    def set_limite_basse(self, valeur):
        """
            Mutateur de l'attribut __limite_basse

            :param valeur: nouvelle valeur pour l'attribut __limite_basse
            :type valeur: long
        """

        self.__limite_basse = valeur

    # ==================================
    def set_limite_droite(self, valeur):
        """
            Mutateur de l'attribut __limite_droite

            :param valeur: nouvelle valeur pour l'attribut __limite_droite
            :type valeur: long
        """

        self.__limite_droite = valeur

    # =========================================
    def set_donnees_image(self, image_chargee):
        """
            Mutateur de l'attribut __donnees_image
            Cette méthode permet de définir les données associée

            :param image_chargee: l'image chargée
            :type image_chargee: numpy.ndarray
        """

        try:

            extraction_des_donnees = image_chargee[self.__limite_haute:self.__limite_basse + 1, self.__limite_gauche:self.__limite_droite + 1].copy()

        except Exception:

            extraction_des_donnees = None
            # message

        self.__donnees_image = extraction_des_donnees

    # =====================================
    def affichage_limites_de_l_image(self):
        """
            Méthode qui permet d'afficher les positions des limites de l'image

            :return: une chaîne de carcatères contenant les positions des limites de l'image
            :rtype: str
        """

        return ("limite haute  : {}\n"
                "limite gauche : {}\n"
                "limite basse  : {}\n"
                "limite droite : {}\n").format(self.__limite_haute, self.__limite_gauche, self.__limite_basse, self.__limite_droite)

    # ========================
    def affichage_image(self):
        """
            Méthode qui permet d'afficher l'image
        """

        try:

            plt.imshow(self.__donnees_image)
            plt.show()

        except Exception:

            pass
        # message

# ==================================================================================================
# FONCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

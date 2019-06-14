# coding=utf-8

"""
    Module qui permet de centraliser/gérer les images à traiter
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

from Sepim.modules.gestionnaire_d_image import GestionnaireDImage
import os
import glob
import numpy

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ==========================================
class GestionnaireDesImagesATraiter(object):
    """
        Classe qui permet des gérer les images à charger

        :ivar __liste_des_images_a_traiter:liste des images créées
        :type __liste_des_images_a_traiter: list[ObjetImage]

        :ivar __dico_des_images_a_traiter: un dictionnaire contenant les images à traiter
        :type __dico_des_images_a_traiter: dict[GestionnaireDImage]

        :ivar __dossier_contenant_les_images: emplacement des images à charger
        :type __dossier_contenant_les_images: str

        :ivar __extensions_prises_en_charge: liste des extensions prises en charge
        :type __extensions_prises_en_charge: tuple(str)

        :ivar __couleur_de_separation: couleur de séparation entre les sous-images d'une image
        :type __couleur_de_separation: numpy.ndarray
    """

    # =================
    def __init__(self):
        """
            Constructeur de la classe
        """

        self.__liste_des_images_a_traiter = []
        self.__dico_des_images_a_traiter = {}
        self.__dossier_contenant_les_images = "../Donnees"
        self.__extensions_prises_en_charge = ("*.png", )
        self.__couleur_de_separation = numpy.array([181, 230, 29])
        # envisager un séparateur magenta plutôt que vert ?

    # ======================================
    def get_dico_des_images_a_traiter(self):
        """
            Accesseur de l'attribut __dico_des_images_a_traiter

            :return une liste contenant les noms des images à traiter
            :rtype dict[ObjetImage]
        """

        return self.__dico_des_images_a_traiter

    # ===========================================
    def lancement_du_traitement_des_images(self):
        """
            Méthode qui lance le traitement des images à traiter
        """

        # Listage des images à traiter
        self.listage_des_images_a_traiter()

        # Création des gestionnaires d'images
        self.creation_des_gestionnaires_d_images()

        # Itération sur les images à traiter
        for nom_image_a_traiter, gestionnaire_de_l_image_a_traiter in self.__dico_des_images_a_traiter.items():

            # Chargement de l'image
            gestionnaire_de_l_image_a_traiter.chargement_de_l_image_a_traiter()

            # Calcul des dimensions de l'image chargée
            gestionnaire_de_l_image_a_traiter.calcul_dimensions_image_chargee()

            # Extractions des sous-images
            gestionnaire_de_l_image_a_traiter.extraction_des_sous_images()

            # Rotation des sous-images
            gestionnaire_de_l_image_a_traiter.rotation_des_sous_images()

            # Sauvegarde des images
            gestionnaire_de_l_image_a_traiter.sauvegarde_des_sous_images()

    # =====================================
    def listage_des_images_a_traiter(self):
        """
            Méthode qui permet de lister les images à traiter
            Cette méthode va parcourir le dossier indiqué via l'attribut "__dossier_contenant_les_images"
            et va récupérer les noms de tous les fichiers dont l'extension ficgure dans l'attribut "__extensions_prises_en_charge"
        """

        # Récupération du dossier courant
        dossier_avant_deplacement = os.getcwd()

        # Déplacement dans le dossier qui contient les images à traiter
        try:

            os.chdir(self.__dossier_contenant_les_images)

        except Exception:

            pass
            # gérer l'exception si le dossier n'existe pas

        # Récupération de la liste des images à traiter selon les extensions spécifiées via l'attribut "__extensions_prises_en_charge"
        for extension in self.__extensions_prises_en_charge:

            self.__liste_des_images_a_traiter.extend(glob.glob(extension))

        # Retour dans le dossier courant
        os.chdir(dossier_avant_deplacement)

    # ============================================
    def creation_des_gestionnaires_d_images(self):
        """
            Méthode qui permet de créer autant de gestionnaires d'image qu'il y a d'image à traiter
        """

        for image_a_traier in self.__liste_des_images_a_traiter:

            self.__dico_des_images_a_traiter[image_a_traier] = GestionnaireDImage(image_a_traier, self.__dossier_contenant_les_images, self.__couleur_de_separation)

# ==================================================================================================
# FONCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

import json
import os

class user_credentials :

    def __init__(self):
        """
        Objet pour enregistrer et configurer les différentes sources de données
        lues avec valemo_data_query.
        """
        self.__dirname = os.path.dirname(__file__)
        self.__file_path = self.__dirname + "/user_credentials.json"
        self.__credential_dict = self.__read_credential()


    def __read_credential(self):
        self.__dict_credentials = json.load(open(self.__file_path,
                                                 "r"))

    @property
    def get_credentials(self):
        """
        Retourne le dictionnaire contenant les credentials enregistrés.
        """
        return self.__dict_credentials

    def add_data_source(self,datasource:dict,sourcename:str):
        """
        Ajoute une source de données au dictionnaire de la librairie.
        """
        self.__dict_credentials[sourcename] = datasource
        json.dump(self.__dict_credentials,
                    open(self.__file_path,"w"))

    def clear_credentials(self):
        """
        Réinitialise tous les mots de passe et sources. Opération irréversible.
        """
        json.dump({},
                open(self.__file_path,"w"))


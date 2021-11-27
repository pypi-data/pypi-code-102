import requests
import random
import pickle
import json

class MelodyGenerator:
    url = 'https://ml-dl-models.herokuapp.com/api/melodygenerator/'

    def __init__(self, data = None, path = 'melody.mp3'):
        """
         Args:
            data (dict): It should dictionary with keys = ['keys','default'] where 'keys' is assigned with the notes of music. Data is initial notes through which model will generate entire melody.
            and default is assigned Boolean Value which is True if octave number is not mentioned in notes provided in keys else assigned False. 
        
            path = path to save melody, default value = 'melody.mp3'.
        """

        if data == None:
            cached_data = self.get_cached_notes() # list of cached data
            rand_index = random.randint(0, len(cached_data)-1)
            self.data = cached_data[rand_index]
        else:
            self.data = data
        self.path = path
            


    def generate_melody(self):
        """
        This is Function creates melody in the given path. 
        If path is not specified it create melody with name melody.mp3 in the directory where the python file is executed.

        """
        json_loaded = requests.post(url=self.url, data = self.data).json()
        byte = json_loaded.encode(encoding = 'latin1')
        stream = pickle.loads(byte)
        stream.write('midi',self.path)

    def get_cached_notes(self):
        """
        This function return list of cached notes.

        return:
            cached_data (list): list of cached notes.
        """
        cached_data = requests.get(url=self.url).json()
        return cached_data

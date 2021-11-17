import base64
import os
import json
from clevr.library_helpers import Library_Functions

class Helper():

    def image_learner_object(directory_object):
        if type(directory_object) != dict:
            raise Exception('Parameter directory_object must be a dictionary.')

        learner = {}
        valid_file_types = ['.jpg', '.png', 'jpeg']

        for label, directory in directory_object.items():
            list_of_files = os.listdir(directory)
            
            for files in list_of_files:
                if files.endswith(files):     
                    if label in learner:
                        learner[label].append(Library_Functions.reduce_and_prepare_image(directory + '/' + files))
                    else:
                        learner[label] = [Library_Functions.reduce_and_prepare_image(directory + '/' + files)]
        
        return {'image': learner}


    def sign_endpoint(signature=None):
        if signature == None:
            raise Exception('You must pass your account signature to successfully verify your endpoint.')
              
        return json.dumps({'verified': True, 'signature': signature})

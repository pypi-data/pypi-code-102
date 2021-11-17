import requests
import json
from clevr.library_helpers import Library_Functions

class Athena():
    
    def classification(api_key=None, learning_object=None, input_val=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        if learning_object == None:
            raise Exception("No learning object provided. Please pass a learning object through the learning_object parameter.")
            
        if input_val == None:
            raise Exception("No input value provided. Please pass a prediction object through the input_val parameter.")
        
        else:
            
            if 'image' in learning_object:
                learning_object = Library_Functions.reconstruct_image_learner(learning_object)

            if 'image' in input_val:
                input_val = Library_Functions.reduce_and_prepare_image(input_val['image'])

                request_object = {
                    'api_key': api_key,
                    'learning_object': learning_object,
                    'input_val': {'image': input_val}
                }
            
            if 'text' in input_val:
                request_object = {
                    'api_key': api_key,
                    'learning_object': learning_object,
                    'input_val': {'text': input_val}
                }

            req = requests.post('https://api.clevr-ai.com/v1/athena/classification', data=json.dumps(request_object))
            response = json.loads(req.text)

            if response['status'] == 'success':
                
                return json.dumps(response, indent=4, sort_keys=False)

            else:
                raise Exception(response['message'])
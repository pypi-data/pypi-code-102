import requests
import json
from clevr.library_helpers import Library_Functions

class Layers():
    
    def save(api_key=None, learning_object=None, name=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        if learning_object == None:
            raise Exception("No learning object provided. Please pass a learning object through the learning_object parameter.")
        
        else:
            request_object = {
                'api_key': api_key,
                'learning_object': learning_object
            }

            if name != None:
                request_object['name'] = name
            
            if 'image' in learning_object:
                learning_object = Library_Functions.reconstruct_image_learner(learning_object)
            

            req = requests.post('https://api.clevr-ai.com/v1/athena/layers/build', data=json.dumps(request_object))
            response = json.loads(req.text)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
    

    def query(api_key=None, layerId=None, input_val=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        if layerId == None:
            raise Exception("No layer ID provided. Please pass the ID of the layer you want to query through the layerId parameter")
            
        if input_val == None:
            raise Exception("No input value provided. Please pass a prediction object through the input_val parameter.")
        
        else:

            if 'image' in input_val:
                request_object = {
                    'api_key': api_key,
                    'layerId': layerId,
                    'input_val': {'image': Library_Functions.reduce_and_prepare_image(input_val['image'])}
                }
            else:
                request_object = {
                    'api_key': api_key,
                    'layerId': layerId,
                    'input_val': {'text': input_val}
                }


            req = requests.post('https://api.clevr-ai.com/v1/athena/layers/query', data=json.dumps(request_object))
            response = json.loads(req.text)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
                
    
    
    def list_layers(api_key=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        else:
            request_object = {
                'api_key': api_key
            }

            req = requests.post('https://api.clevr-ai.com/v1/athena/layers/list', data=json.dumps(request_object))
            response = json.loads(req.text)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
                
    
    
    def delete_layer(api_key=None, layerId=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        if layerId == None:
            raise Exception("No layer ID provided. Please pass the ID of the layer you want to delete through the layerId parameter")
            
        else:
            request_object = {
                'api_key': api_key,
                'layerId': layerId
            }

            req = requests.post('https://api.clevr-ai.com/v1/athena/layers/delete', data=json.dumps(request_object))
            response = json.loads(req.text)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
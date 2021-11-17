import json
import requests

class Persona():

    def query(api_key=None, model=None, input_val=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        if model == None:
            raise Exception("No model provided. Please pass a model name through the model parameter.")
            
        if input_val == None:
            raise Exception("No input value provided. Please pass a input string object through the input_val parameter.")
        
        else:
            request_object = {
                'api_key': api_key,
                'model': model,
                'input_val': input_val
            }

            req = requests.post('https://api.clevr-ai.com/persona/query', data=json.dumps(request_object))
            response = json.loads(req)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
    
    
    def list_models(api_key=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        else:
            request_object = {
                'api_key': api_key
            }

            req = requests.post('https://api.clevr-ai.com/persona/list', data=json.dumps(request_object))
            response = json.loads(req)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
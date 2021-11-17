import requests
import json
from clevr.helpers import Helper

class Platform():

    def query(api_key=None, appId=None, input_val=None):

        if api_key == None:
            raise Exception("No API key provided. Please pass your API key through the api_key parameter.")
            
        if appId == None:
            raise Exception("No App ID provided. Please pass the ID of the Platform app you want to query through the appId parameter.")
            
        if input_val == None:
            raise Exception("No input value provided. Please pass a prediction object through the input_val parameter.")
        
        else:

            for input_type, inference_value in input_val.items():
                inference_value = base64.b64encode(inference_value)
                inference_value = inference_value.decode('utf-8')
                input_val[input_type] = inference_value
                break

            request_object = {
                'api_key': api_key,
                'appId': appId,
                'input_val': input_val
            }

            req = requests.post('https://api.clevr-ai.com/platform/query', data=json.dumps(request_object))
            response = json.loads(req)

            if response['status'] == 'success':
                return json.dumps(response, indent=4, sort_keys=True)

            else:
                raise Exception(response['message'])
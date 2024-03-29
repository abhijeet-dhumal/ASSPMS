import requests, os
from decouple import config, Csv

import os
model_id = config('NANONETS_MODEL_ID')
api_key = config('NANONETS_API_KEY')

url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/Train/'

querystring = {'modelId': model_id}

response = requests.request('POST', url, auth=requests.auth.HTTPBasicAuth(api_key, ''), params=querystring)

print(response.text)

print("\n\nNEXT RUN: python ./code/model-state.py")
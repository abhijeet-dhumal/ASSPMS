import requests, os, sys
from decouple import config, Csv
from oauth2_provider import settings as oauth2_settings
import os
model_id = config('NANONETS_MODEL_ID')
api_key = config('NANONETS_API_KEY')

image_path = sys.argv[1]
def license_plate_text_detection(image_path):
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/LabelFile/'

    data = {'file': open(image_path, 'rb'),    'modelId': ('', model_id)}

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)

    js=response.json()
    templates=js['result']
    return templates
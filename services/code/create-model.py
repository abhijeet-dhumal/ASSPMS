import requests, os, json
from decouple import config, Csv
from oauth2_provider import settings as oauth2_settings
import os  
url = "https://app.nanonets.com/api/v2/ObjectDetection/Model/"
api_key = config('NANONETS_API_KEY')

##
payload = "{\"categories\" : [\"number_plate\"], \"model_type\": \"ocr\"}"
headers = {'Content-Type': "application/json",}

response = requests.request("POST", url, headers=headers, auth=requests.auth.HTTPBasicAuth(api_key, ''), data=payload)
print(response.text)
model_id = json.loads(response.text)["model_id"]

print("NEXT RUN: export NANONETS_MODEL_ID=" + model_id)
print("THEN RUN: python nanonets-ocr-sample-python/code/upload-training.py")
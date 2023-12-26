import requests, os, json
from decouple import config, Csv
model_id = config('NANONETS_MODEL_ID')
api_key=config('NANONETS_API_KEY')


url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id

response = requests.request('GET', url, auth=requests.auth.HTTPBasicAuth(api_key,''))

state = json.loads(response.text)["state"]
status = json.loads(response.text)["status"]

if state != 5:
	print("The model isn't ready yet, its status is:", status)
	print("We will send you an email when the model is ready. If you are impatient, run this script again in 10 minutes to check.")
else:
	print("NEXT RUN: python ./code/prediction.py ./images/151.jpg")

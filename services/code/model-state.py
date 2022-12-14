import requests, os, json

model_id = '23c87f52-8176-4877-b510-1105390d321d'

# api_key = os.environ.get('NANONETS_API_KEY')
from decouple import config, Csv
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

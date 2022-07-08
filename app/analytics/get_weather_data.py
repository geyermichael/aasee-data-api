import requests
import pandas as pd
import json
import os

date = '2021-05-18'
last_date = '2022-06-25'
url = 'https://api.brightsky.dev/weather?lat=51.95&lon=7.6&date=' + date + '&' + 'last_date=' + last_date

resp = requests.get(url=url) 
raw_data = resp.json() 
weather_data = raw_data['weather']
with open(os.getcwd() + r'\app\analytics\weather_raw_data.json','w') as f: # save weather data into json file
    json.dump(raw_data, f)
with open(os.getcwd() + r'\app\analytics\weather_data.json','w') as f: # save weather data into json file
    json.dump(weather_data, f)
df_weather = pd.DataFrame.from_records(weather_data)
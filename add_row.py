import requests
import json
import numpy as np
import os
import datetime

import adafruit_dht
from board import D4
dht_device = adafruit_dht.DHT22(D4)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

api_key = '2a3cbd9034962722e522419a7305997c'

# Get outside temperature + humidity

base_url = "http://api.openweathermap.org/data/2.5/weather?"
city = 'New York City'
complete_url = base_url + "appid=" + api_key + "&q=" + city

try:
    resp = requests.get(complete_url)

    current_temp_k = resp.json()['main']['temp']
    current_temp_f = np.round((current_temp_k - 273.15) * (9/5) + 32, 2)
    current_humidity = resp.json()['main']['humidity']
except:
    current_temp_f = -1000
    current_humidity = -1000

# Get internal temps

def get_temp_hum(dht_device):
    count = 0
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None or humidity is not None:
                return {
                    'temperature': (temperature * (9/5)) + 32,
                    'humidity': humidity
                }
            else:
                pass

        except:
            count += 1
            if count == 1000:
                return {
                    'temperature': 0,
                    'humidity': 0
                }
            pass

internals = get_temp_hum(dht_device)

# Authorize gspread

feedsURL = 'https://spreadsheets.google.com/feeds'
driveURL = 'https://www.googleapis.com/auth/drive'
scope = [feedsURL, driveURL]

filepath = '/home/pi/google_credentials/gspread-329ef1b5ac67.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    filepath, scope)
gc = gspread.authorize(credentials)

wb = gc.open('apt_temp')

sh = wb.sheet1

# Add new row

current_datetime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')

sh.append_row([
    current_datetime, current_temp_f, internals['temperature'],
    current_humidity, internals['humidity']
])

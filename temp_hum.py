import requests
import json
import numpy as np
import os
import datetime

import Adafruit_DHT
dht_device = adafruit_dht.DHT22(D4)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

api_key = '2a3cbd9034962722e522419a7305997c'

base_url = "http://api.openweathermap.org/data/2.5/weather?"
city = 'New York City'
complete_url = base_url + "appid=" + api_key + "&q=" + city

sensor = Adafruit_DHT.DHT22
pin = 18

def get_temp_hum(dht_device):
    count = 0
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
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

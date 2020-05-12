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

base_url = "http://api.openweathermap.org/data/2.5/weather?"
city = 'New York City'
complete_url = base_url + "appid=" + api_key + "&q=" + city

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

# Robert Jones
# 10.20.23
# Geocoder Class w/out Bing

import pandas as pd
import numpy as np
import urllib
import requests
import json
import time
import func_timeout

class Geocode():

    def __init__(self,read_file):

        if str(read_file).split('.')[-1] == 'csv':
            # Open csv file
            df = pd.read_csv(read_file)
        elif str(read_file).split('.')[-1] == 'xlsx':
            # Open xlsx file
            df = pd.read_excel(read_file)
        
        for index, row in df.iterrows():
            coordinates = Geocode.geolocate(Geocode.clean_address(row['address']),row['city'],'CA',str(row['zip']))
            lng,lat = coordinates['x'],coordinates['y']
            data = [index,lat,lng]
            df_coordinate = pd.DataFrame(data=[data],columns=['index','lat','lng'])
            df_coordinate.to_csv('geocoded_2023_batteries_delivered.csv',mode='a',index=False,header=False)

    def clean_address(address):
        building_type = ['APT','BLDG','BSMT','DEPT','FL','FRNT','HNGR','LBBY','LOT','LOWR','OFC','PH','PIER','REAR','RM','SIDE','SLIP','SPC','STE','STOP','TRLR','UNIT','UPPR']
        for x in range(len(building_type)):
            if building_type[x] in address:
                address = address.split(building_type[x])[0]
                return address
            else:
                return address

    def geolocate(ServiceAddress,ServiceCity,ServiceState,ServiceZipCode):
            ServiceAddress = urllib.parse.quote(ServiceAddress)
            ServiceCity = urllib.parse.quote(ServiceCity)
            ServiceZipCode = urllib.parse.quote(str(ServiceZipCode))
            ServiceState = urllib.parse.quote(ServiceState)

            full_address = f'{ServiceAddress},%20{ServiceCity},%20{ServiceState},%20{ServiceZipCode}'
            base_url = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?benchmark=Public_AR_Current&vintage=Current_Current&layers=0&format=json&address='            
            
            try:
                def query_api():
                    result = requests.get(base_url+full_address).text
                    time.sleep(.5)
                    return result
                def time_controller(max_wait_time):
                    try:
                        result = func_timeout.func_timeout(max_wait_time,query_api)
                        return result
                    except func_timeout.FunctionTimedOut:
                        print('API call timed out')
                    
                # If API call last longer than 1.5 seconds, terminate the call
                result = time_controller(1.5)
                result = json.loads(result)
                coordinates = result['result']['addressMatches'][0]['coordinates']
                print(f'Found {full_address}: {coordinates["x"]},{coordinates["y"]}')
                return coordinates

            except Exception as e:
                print(f'Exception Found locating address: {e}')
                print(f'Could not find {full_address}')
                return {'x':None,'y':None}


read_file = 'C:/Users/Robert.Jones/OneDrive - Central Coast Energy Services, Inc/Documents/data_sheet/2023_batteries_delivered.xlsx'
Geocode(read_file=read_file)
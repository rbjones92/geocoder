# Robert Jones
# 3.8.23
# GeoCode Battery Deliveries From 2022

import pandas as pd
import geocoder
key = open('bing_key.txt','r')
key = key.readline()



def geolocate(ServiceAddress,ServiceCity,ServiceZipCode,ServiceState):
    
    full_address = f'{ServiceAddress}, {ServiceCity}, {ServiceZipCode}, {ServiceState}'

    try:
        g = geocoder.bing(full_address,key=key)
        results = g.json
        lat = results['lat']
        lng = results['lng']
        print(f'Address = {full_address} Latitude = {lat} Longitude = {lng}')

        return lat,lng

    except:
            print(f'Could not find {full_address}')
            return 

df = pd.read_excel('batts_delivered_2022.xlsx')

df['lat_lng'] = df.apply(lambda x: geolocate(x['address'], x['city'], x['zip'], x['state']), axis=1)

df.to_excel('geocoded_batts_delivered_2022.xlsx')


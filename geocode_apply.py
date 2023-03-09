import pandas as pd
import geocoder 
key = open('bing_key.txt','r')
key = key.readline()

def geolocate_lat(ServiceAddress,ServiceCity,ServiceZipCode,ServiceState):
    
    full_address = f'{ServiceAddress}, {ServiceCity}, {ServiceZipCode}, {ServiceState}'

    try:
        g = geocoder.bing(full_address,key=key)
        results = g.json
        lat = results['lat']
        print(f'found latitude {lat}')
        return lat

    except:
            print(f'Could not find {full_address}')
            return 


def geolocate_long(ServiceAddress,ServiceCity,ServiceZipCode,ServiceState):
      
    full_address = f'{ServiceAddress}, {ServiceCity}, {ServiceZipCode}, {ServiceState}'

    try:
        g = geocoder.bing(full_address,key=key)
        results = g.json
        lng = results['lng']
        print(f'found longitude {lng}')
        return lng

    except:
            print(f'Could not find {full_address}')
            return


df = pd.DataFrame({'ServiceAddress': '10397 PIERI CT','ServiceCity':'MOSS LANDING','ServiceZipCode':'95039','ServiceState':'CA'},index=['test_address'])

df['latidude'] = df.apply(lambda x: geolocate_lat(x['ServiceAddress'], x['ServiceCity'], x['ServiceZipCode'], x['ServiceState']), axis=1)

df['longitude'] = df.apply(lambda x: geolocate_long(x['ServiceAddress'], x['ServiceCity'], x['ServiceZipCode'], x['ServiceState']), axis=1)

print(df)


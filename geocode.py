import pandas as pd
import geocoder 
key = open('bing_key.txt','r')
key = key.readline()

# Open ServTraq Data
pd_df = pd.read_csv('liheap_2008_to_2022.csv')

# Initialize not_caught dictionary for exceptions
not_caught = {}

# Iterate thru rows of ServTraq
for index, row in pd_df.iterrows():
        
        # Get Address Data
        address = row["ServiceAddress"]
        city = row["ServiceCity"]
        zip = row["ServiceZipCode"]
        state = "CA"
        full_address = f'{address}, {city}, {state} {zip}'

        # Geolocate in try/except block
        try:
            g = geocoder.bing(full_address, key=key)
            results = g.json
            lat = results['lat']
            lng = results['lng']
            pd_df.loc[index,['latitude']] = lat
            pd_df.loc[index,['longitude']] = lng
            print(f'found {full_address}...{lat},{lng}')

        # Add exceptions to not_caught dictionary, then continue
        except:
              print(f'Could not find {full_address} at {index}')
              not_caught[index] = full_address
              continue


not_caught_df = pd.DataFrame.from_dict(not_caught,orient='index')
# not_caught_df.to_csv('liheap_2008_to_2022_geocode_not_caught.csv')

# Write file
# pd_df.to_csv('liheap_2008_to_2022_geocode.csv')


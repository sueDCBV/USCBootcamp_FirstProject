# Dependencies
import requests
import json
import pandas as pd

# Google developer API key
from config import gkey1

# Target city #### Getting coordinates from Geogle GeoCoding API ###API 1
city_address=pd.read_csv('../Raw_Data/1-1.city_codes.csv',sep=',')

#grab LA County Data
LA_cities=city_address[city_address['Metro']=='Los Angeles']

# list of 20 top cities by population in LA County

list_city=['Los Angeles',
'Long Beach',
'Santa Clarita',
'Glendale',
'Palmdale',
'Lancaster',
'Pomona',
'Torrance',
'Pasadena',
'Inglewood',
'El Monte',
'Downey',
'West Covina',
'Norwalk',
'Burbank',
'Compton',
'South Gate',
'Whittier',
'Hawthrone',
'Alhambra']

LA_cities.head()

#Pull City and state
final=[]
for i in range(len(LA_cities)):
    target=LA_cities.iloc[i,:]
    table_final={}
    table_final['Region']=target['Region']
    table_final['State']=target['State']
    if table_final['Region'] in list_city:
        final.append(table_final)
final = pd.DataFrame(final)
final
#regions=pd.DataFrame(final)
list_Region=final['Region']
list_Region

# Grab Lat and Lng from google 
# Run a request to endpoint and convert result to json
target=[]
for i in range(len(list_Region)):
    
    target_city=list_Region[i]
    target_url = "https://maps.googleapis.com/maps/api/geocode/json?" \
     "address=%s&key=%s" % (target_city, gkey1)
    geo_data = requests.get(target_url).json()
    #print(geo_data)
    R1=geo_data["results"][0]
    #print(R1)
    for a in range(len(R1)):
        R2=R1["geometry"]
        print(R2['location']['lat'])
        for j in R2:
            citi={}
            citi['lat']=R2["location"]["lat"]
            citi['lng']=R2["location"]["lng"]
            citi['northeast_Lat']=R2["bounds"]["northeast"]["lat"]
            citi['northeast_Lng']=R2["bounds"]["northeast"]["lng"]
            citi['southwest_Lat']=R2["bounds"]["southwest"]["lat"]
            citi['southwest_Lng']=R2["bounds"]["southwest"]["lng"]
            citi['address']=target_city
    target.append(citi)

# create dataframe to store all lat and lng data
address_coordinate=pd.DataFrame(target)
address_coordinate

#save address_coordinate for later use
address_coordinate.to_csv('../Raw_Data/1-1.LA_cities_Lat_lng_codes_data.csv',sep=',', index=None)


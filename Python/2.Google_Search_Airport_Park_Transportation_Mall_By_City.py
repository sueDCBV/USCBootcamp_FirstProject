#Using Google Search to obtain closest amenities by cities
# code by Sue Del Carpio Bellido

# Dependencies
import requests
import json
import pandas as pd


# Google developer API key
from config import gkey_places

file_one = "../Raw_Data/1-1.LA_cities_Lat_lng_codes_data.csv"
cities_tot_df = pd.read_csv(file_one, encoding = "ISO-8859-1")

cities_tot_df = cities_tot_df.rename(columns={"address":"City"})
cities_tot_df

#Filter only selected cities for analysis
selected_cities=['Alhambra','Burbank','Inglewood','Glendale','Long Beach','Los Angeles','Palmdale','Pasadena','Santa Clarita','Torrance']
cities_df=cities_tot_df[cities_tot_df['City'].isin(selected_cities)]
cities_df

# AIRPORTS close to cities
cities_df["airport"]=None

base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

for index, row in cities_df.iterrows():
    target_coordinates = str(row["lat"]) +","+str(row["lng"]) 
    target_radius = 5000
    target_type = "airport"
    #target_keyword ="airport"

    params = {
        "location": target_coordinates,
        "radius": target_radius,
        "type": target_type,
        "key": gkey_places}
        #"keyword": target_keyword}

    response = requests.get(base_url, params=params)
    airport_data = response.json()

    #print(json.dumps(airport_data, indent=4, sort_keys=True))

    counter = 0
    for airport in airport_data["results"]:
        #print(airport["name"])
        #print(airport["vicinity"])
        #print(airport["name"].upper().find("AIRPORT"))
        
        if airport["name"].upper().find("AIRPORT")>0:
            counter += 1
            
        
    cities_df.set_value(index,"airport",counter)
cities_df

# PUBLIC TRANSPORTATION close to cities
cities_df["public_transportation"]=None

base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

for index, row in cities_df.iterrows():
    target_coordinates = str(row["lat"]) +","+str(row["lng"]) 
    target_radius = 8000
    target_type = ["light_rail_station",
                "transit_station","subway_station"]
    #target_keyword ="bank"

    params = {
        "location": target_coordinates,
        "radius": target_radius,
        "type": target_type,
        "key": gkey_places}
        #"keyword": target_keyword}

    response = requests.get(base_url, params=params)
    train_data = response.json()

    #print(json.dumps(train_data, indent=4, sort_keys=True))

    counter = 0
    for train in train_data["results"]:
        #print(train["name"])
        #print(train["vicinity"])
        counter += 1
        
    cities_df.set_value(index,"public_transportation",counter)
cities_df

# PARKS close to cities
cities_df["park"]=None

base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

for index, row in cities_df.iterrows():
    target_coordinates = str(row["lat"]) +","+str(row["lng"]) 
    target_radius = 8000
    target_type = "park"
    #target_keyword ="bank"

    params = {
        "location": target_coordinates,
        "radius": target_radius,
        "type": target_type,
        "key": gkey_places}
        #"keyword": target_keyword}

    response = requests.get(base_url, params=params)
    park_data = response.json()

    #print(json.dumps(park_data, indent=4, sort_keys=True))

    counter = 0
    for park in park_data["results"]:
        #print(park["name"])
        #print(park["vicinity"])
        #print(park["rating"])
        #if park["rating"]>3:
        counter += 1
                
    cities_df.set_value(index,"park",counter)
cities_df

# SHOPPING MALLS close to cities
cities_df["shopping_mall"]=None

base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

for index, row in cities_df.iterrows():
    target_coordinates = str(row["lat"]) +","+str(row["lng"]) 
    target_radius = 5000
    target_type = "shopping_mall"
    #target_keyword ="bank"

    params = {
        "location": target_coordinates,
        "radius": target_radius,
        "type": target_type,
        "key": gkey_places}
        #"keyword": target_keyword}

    response = requests.get(base_url, params=params)
    shopping_mall_data = response.json()

    #print(json.dumps(shopping_mall_data, indent=4, sort_keys=True))

    counter = 0
    for shopping_mall in shopping_mall_data["results"]:
        #print(shopping_mall["name"])
        #print(shopping_mall["vicinity"])
        #print(shopping_mall["rating"])
        
        try:
            if shopping_mall["rating"]>4:
                counter += 1
        except KeyError:
            continue
        
                
    cities_df.set_value(index,"shopping_mall",counter)
cities_df.head()

# Visualize the DataFrame
cities_df
cities_dfb=cities_df[['City','public_transportation','park','shopping_mall','airport']]
cities_dfb.head()

##Unpivot data for Seaborn plots
##Code by Lindsay Yang
cities_dfc=pd.melt(cities_dfb, id_vars=['City'], value_vars=['public_transportation', 'park','shopping_mall','airport'])

cities=cities_dfb[['City']]

import seaborn as sns
import matplotlib.pyplot as plt


sns.set_style("whitegrid")
plt.figure(figsize=(20,8))
sns.barplot(x='City', y='value', hue='variable', data=cities_dfc)
plt.xticks(rotation=90)

plt.ylabel('count of amenities')
plt.title('Amenities in LA cities')
# Save the figure
plt.savefig("../Clean_Data/2.Amenities_by_city.png")
plt.show()
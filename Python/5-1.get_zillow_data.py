# ZILLOW DATA EXTRACTION WRITTEN BY SONIA YANG

# Dependencies
import requests
import urllib
import random
import math
import pandas as pd
import xml.etree.ElementTree as ET
import time
from config import zws_id, gkey # please use your own Zillow & Google API keys!
from urllib.request import urlopen

# FUNCTION to grab the exact address based on longitude and latitude
# modified from here https://gist.github.com/bradmontgomery/5397472
# their example didn't include an API key, but I added it otherwise you'd hit the rate limit easily

def reverse_geocode(latitude, longitude):
    # Did the geocoding request comes from a device with a
    # location sensor? Must be either true or false
    sensor = 'true'

    # Hit Google's reverse geocoder directly
    # NOTE: I *think* their terms state that you're supposed to
    # use google maps if you use their api for anything.
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}&key={key}".format(
        lat=latitude,
        lon=longitude,
        sen=sensor,
        key=gkey
    )
    url = "{base}{params}".format(base=base, params=params)
    #print(url)
    response = requests.get(url).json()
    address = response['results'][0]['formatted_address']
    return address
    
# FUNCTION to generate random lat & lng within a certain radius 
# modified from here: http://hadoopguru.blogspot.com/2014/12/python-generate-random-latitude-and.html
# changed to take in an empty initial dataframe and load in the data + return it
# this calls the reverse geocode function to grab the addresses of each randomly generated lat & lng

def generate_addresses(latitude, longitude, df):
    
    radius = 5000                         #Choose your own radius
    radiusInDegrees=radius/111300            
    r = radiusInDegrees

    counter = 0
    
    for i in range(1,50):                 #Choose number of Lat Long to be generated

        u = float(random.uniform(0.0,1.0))
        v = float(random.uniform(0.0,1.0))

        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t) 
        y = w * math.sin(t)

        xLat  = x + latitude
        yLng = y + longitude

        df.set_value(counter, "latitude", xLat)
        df.set_value(counter, "longitude", yLng)
        
        #print(format(counter) + ": " + format(xLat) + ", " + format(yLng))
        address = reverse_geocode(xLat, yLng).split(',')
        citystatezip = address[1] + address[2]
        
        df.set_value(counter, "address", address[0])
        df.set_value(counter, "city_state_zip", citystatezip)
        
        # Add to counter
        counter = counter + 1
    
    return df
    
# FUNCTION to call Zillow API's GetSearchResults and will check to see if a house exists at that address
# message code will be written to dataframe
# zillow url format
# http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
        
def get_message_codes(df):

    for index, row in df.iterrows():

        try:
            url = 'https://www.zillow.com/webservice/GetSearchResults.htm?zws-id='
            address = row['address']
            citystatezip =row['city_state_zip']


            query_url = url + zws_id + '&address=' + urllib.parse.quote(address) + '&citystatezip=' + urllib.parse.quote(citystatezip) 
            #print(query_url)

            root = ET.parse(urlopen(query_url)).getroot()

            for message in root.iter('message'):
                message_code = message[1].text

            print(format(index) + ": " + message_code)

            df.set_value(index, 'message_code', message_code)

            time.sleep(0.5) #necessary bc bombarding Zillow with API calls doesn't allow enough time to respond to each

        except:
            break
    
# FUNCTION to call Zillow's GetDeepSearchResults and look up Zestimate, bed, and bath
# http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
# there are some limitations such as multiple zestimates depending on when the house was sold/if it was sold multiple times
# the code to handle that would get too convoluted so I am just writing in the most recent (according to the API) values
# probably not what we would do in real life
# but a decision we made re: the scope of a classroom project on a short time constraint

def search_zillow(df):
    
    for index, row in df.iterrows():
        try:
            url = 'https://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id='
            address = df['address'][index]
            citystatezip = df['city_state_zip'][index]


            query_url = url + zws_id + '&address=' + urllib.parse.quote(address) + '&citystatezip=' + urllib.parse.quote(citystatezip) 


            root = ET.parse(urlopen(query_url)).getroot()

            print("row " + format(index) + ": " + address + citystatezip)
            print(query_url)

            '''
               "year built","lot size","finished sq ft"'''
            
            #zpid
            for zpid in root.iter('zpid'):
                df.set_value(index,'zpid', zpid.text)
            
            # we already have the address from the address + citystatezip variables
            # so we don't need to grab it again
            # same with lat & lng already being in the table
            
            #valuation (high and low)
            for valuation in root.iter('valuationRange'):
                highValuation = valuation[1].text
                lowValuation = valuation[0].text
                df.set_value(index, 'valuation_high', highValuation)
                df.set_value(index, 'valuation_low', lowValuation)
            
            #zestimate
            for zestimate in root.iter('zestimate'):
                zestimate_value = zestimate[0].text

                if zestimate_value is None:
                    print('not for sale')
                else:
                    print ('zestimate (value): ' + format(zestimate[0].text)) 
                    df.set_value(index, 'zestimate', zestimate_value)
             
            #home value index
            for zindexValue in root.iter('zindexValue'):
                df.set_value(index, 'home value index', zindexValue.text)
            
            #tax assessment
            for taxAssessment in root.iter('taxAssessment'):
                df.set_value(index, 'tax assessment', taxAssessment.text)
                
            #tax assessment year
            for taxAssessmentYear in root.iter('taxAssessmentYear'):
                df.set_value(index, 'tax assess year', taxAssessmentYear.text)
                
            #year built
            for yearBuilt in root.iter('yearBuilt'):
                df.set_value(index, 'year built', yearBuilt.text)
             
            #lot size sq ft
            for lotSizeSqFt in root.iter('lotSizeSqFt'):
                df.set_value(index, 'lot size', lotSizeSqFt.text)
            
            #finished sq ft
            for finishedSqFt in root.iter('finishedSqFt'):
                df.set_value(index, 'finished sq ft', finishedSqFt.text)
            
            #bedrooms
            for bedroom in root.iter('bedrooms'):
                bedrooms = bedroom.text
                #print("bedrooms: " + bedrooms)
                df.set_value(index, 'bedrooms', bedrooms)

            #bathrooms
            for bathroom in root.iter('bathrooms'):
                bathrooms = bathroom.text
                #print("bathrooms: " + bathrooms + "\n")
                df.set_value(index, 'bathrooms', bathrooms)           
            
            print('\n')

            time.sleep(0.5) 


        except:
            break

# Read cities file to pull the Latitude and Longtitude
Cities=pd.read_csv('../Raw_Data/1-1.LA_cities_Lat_lng_codes_data.csv')
print(f'{Cities["address"]}')
city1 = input("Please input first city your want to pull data")
selectcity = Cities.loc[Cities["address"] == city1, :]
LAT = selectcity.iloc[0,1]
LNG = selectcity.iloc[0,2]

# HOW TO RUN ALL THE FUNCTIONS, USING LOS ANGELES AS AN EXAMPLE

# coordinates taken from the CitiesGeo_Output.csv
# we should manually run the following code on each individual city instead of nesting it in another loop
# while this may be hardcoded, it's better than waiting on one gigantic loop that takes forever

# STEP 1: INITALIZE THE DATAFRAME
# if we need any more fields, let me know
la_df = pd.DataFrame({"zpid": '',
                      "address":'',
                      "city_state_zip":'',
                      "latitude":'',
                      "longitude":'',
                      "message_code":'',
                      "zestimate":'',
                      "valuation_high":'',
                      "valuation_low": '',
                      "home value index":'',
                      "tax assessment":'',
                      "tax assess year":'',
                      "year built":'',
                      "lot size":'',
                      "finished sq ft":'',
                      "bedrooms":'',
                      "bathrooms":''}, index=[0])

# reorder the columns
la_df = la_df[["zpid", "address","city_state_zip","latitude","longitude","message_code","zestimate",
               "valuation_high","valuation_low","home value index","tax assessment","tax assess year",
               "year built","lot size","finished sq ft","bedrooms","bathrooms"]]

# STEP 2: GENERATE RANDOM ADDRESSES IN THE DESIGNATED AREA
# pass in the coordinates for Los Angeles plus the empty dataframe
generate_addresses(LAT,LNG, la_df) 

#la_df

# STEP 3: CALL THE ZILLOW API TO GET MESSAGE CODES
# 0 means there is a valid property at that address
# 508 and anything else means there isn't
# if you get nothing but invalid message codes, re-run STEP 2
# you might have to sign up for a new Zillow account if you keep getting invalid results here
# there is a possibility you hit the rate limit

get_message_codes(la_df)

# STEP 4: DROP INVALID ENTRIES FROM DATAFRAME 
# cull all the rows where houses do not exist at the address
# take what is valid (message code of '0')
# the code sometimes might break/not get a response from the server so it's better to take what IS valid

la_df = la_df[la_df.message_code == '0']

# take out items that does not belong to the select city
la_df=la_df[la_df.city_state_zip.str.contains(city1) == True]

la_df

# STEP 5: SEARCH ZILLOW AND GET ZESTIMATE, BEDROOMS, & BATHROOMS
# fill the dataframe with the data

search_zillow(la_df)
la_df

# do any further data cleaning you need to yourself
# for example, dropping any rows with NaN values
la_df = la_df.dropna(axis=0, how='any')
la_df

# maybe write to CSV to store the data for usage later/before doing plots? so you don't have to rerun everything

# review current data and see if more data is needed (at least 50 valid data per city)
add_df = pd.DataFrame(la_df)
final_df = add_df
final_df = final_df.reset_index(drop=True)
len(final_df)

# If minimum 50 valid data counts is not met, we will loop through the codes above to make sure we have sufficient data
while(len(final_df)<50):
    generate_addresses(LAT,LNG, la_df) 
    get_message_codes(la_df)
    la_df = la_df[la_df.message_code == '0']
    la_df=la_df[la_df.city_state_zip.str.contains(city1) == True]
    search_zillow(la_df)
    la_df = la_df.dropna(axis=0, how='any')
    add_df = add_df.append(la_df, ignore_index=True)
    final_df = add_df.drop_duplicates()
len(final_df)

# review final city data before save the file
final_df.head()

# Save file into Clean Data folder
final_df.to_csv(f'../Clean_Data/5-1.{city1}_zillow_data.csv')
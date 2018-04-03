# ZILLOW DATA Combined
# Dependencies
import numpy as np
import math
import pandas as pd
import time
import requests
import urllib
import random
import xml.etree.ElementTree as ET
from config import zws_id # please use your own Zillow API keys!
from urllib.request import urlopen

# Read all zillow files by cities
Burbank_df=pd.read_csv('../Clean_Data/5-1.Burbank_zillow_data.csv')
Glendale_df=pd.read_csv('../Clean_Data/5-1.Glendale_zillow_data.csv')
Inglewood_df=pd.read_csv('../Clean_Data/5-1.Inglewood_zillow_data.csv')
Alhambra_df=pd.read_csv('../Clean_Data/5-1.Alhambra_zillow_data.csv')
Longbeach_df=pd.read_csv('../Clean_Data/5-1.Long Beach_zillow_data.csv')
Losangeles_df=pd.read_csv('../Clean_Data/5-1.Los Angeles_zillow_data.csv')
Palmdale_df=pd.read_csv('../Clean_Data/5-1.Palmdale_zillow_data.csv')
Pasadena_df=pd.read_csv('../Clean_Data/5-1.Pasadena_zillow_data.csv')
Santaclarita_df=pd.read_csv('../Clean_Data/5-1.Santa Clarita_zillow_data.csv',encoding = "ISO-8859-1")
Torrance_df=pd.read_csv('../Clean_Data/5-1.Torrance_zillow_data.csv')


# Combine all dataframe into one master dataframe
final_df = Burbank_df
final_df = final_df.append(Glendale_df, ignore_index=True)
final_df = final_df.append(Inglewood_df, ignore_index=True)
final_df = final_df.append(Alhambra_df, ignore_index=True)
final_df = final_df.append(Longbeach_df, ignore_index=True)
final_df = final_df.append(Losangeles_df, ignore_index=True)
final_df = final_df.append(Palmdale_df, ignore_index=True)
final_df = final_df.append(Pasadena_df, ignore_index=True)
final_df = final_df.append(Santaclarita_df, ignore_index=True)
final_df = final_df.append(Torrance_df, ignore_index=True)
final_df

# reorder the columns
final_df = final_df[["zpid", "address","city_state_zip","latitude","longitude","message_code","zestimate",
               "valuation_high","valuation_low","home value index","tax assessment","tax assess year",
               "year built","lot size","finished sq ft","bedrooms","bathrooms"]]
# drop any NA/Null number/row
final_df = final_df.dropna(axis=0, how='any')
final_df

#add in new columns to store new values
final_df['rentzestimate'] =''
final_df['valuechange'] =''
final_df.head()

# define function to pull 30 day value change and rentestimate
def search_zillow(df):
    
    for index, row in df.iterrows():
        try:
            url = 'https://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id='
            address = df['address'][index]
            citystatezip = df['city_state_zip'][index]


            query_url = url + zws_id + '&address=' + urllib.parse.quote(address) + '&citystatezip=' + urllib.parse.quote(citystatezip) +'&rentzestimate=true' 


            root = ET.parse(urlopen(query_url)).getroot()

            print("row " + format(index) + ": " + address + citystatezip)
            

            #30dayvaluechange
            for zestimate in root.iter('zestimate'):
                valuechange_value = zestimate[3].text

                if valuechange_value is None:
                    print('not available')
                else:
                    print ('30 day value change: ' + format(zestimate[3].text)) 
                    df.set_value(index, 'valuechange', valuechange_value)
                    
            #rentzestimate
            for rentzestimate in root.iter('rentzestimate'):
                rentzestimate_value = rentzestimate[0].text

                if rentzestimate_value is None:
                    print('not for rent')
                else:
                    print ('rentzestimate (value): ' + format(rentzestimate[0].text)) 
                    df.set_value(index, 'rentzestimate', rentzestimate_value)
            
            print('\n')

            time.sleep(0.5) 


        except:
            break
            
#use function to pull rent estimate and 30 day price change
search_zillow(final_df)

# check new dataframe
final_df.head()

# Save file into Clean Data folder
final_df.to_csv(f'../Clean_Data/5-2.Combined_zillow_data.csv')
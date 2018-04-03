# Dependencies
import requests
import json
import pandas as pd

# Google developer API key (this key is obtained from https://www.zipcodeapi.com/API,
#the API code is temporate, need to grab a new one)
from config import zipkey
# read lag/lng data
LA_counties=pd.read_csv('../Raw_Data/1-1.LA_cities_Lat_lng_codes_data.csv',sep=',')
LA_counties.head()

list_address=LA_counties[['address']]

County=list_address['address']
State='CA'

County

###Get the list of Counties to get zipcode
list2=[]
for i in range(len(County)):
    
    target=County[i]
    t_state=State
    target_url="https://www.zipcodeapi.com/rest/"+zipkey+"/city-zips.json/"+target+"/"+t_state
    list2.append(target_url)

#show api link
list2[0]

# Run a request to endpoint and convert result to json
target=[]

for i in range(len(County)):
   
    target_city=County[i]          
    target_url = list2[i]
    geo_data = requests.get(target_url).json()
    print (geo_data)
    R1=geo_data["zip_codes"]
    for j in range(len(R1)):
        dic={}
        dic['County']=target_city
        dic['zip']=R1[j] 
        target.append(dic)

# Save zip code by city file 
Table=pd.DataFrame(target)
Table.to_csv('../Raw_Data/1-2.zipcodes_in_LA_counties.csv',index=None)
Table

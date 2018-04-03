import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns, numpy as np
from itertools import cycle, islice

##Loading Data in
import pandas as pd
zillow=pd.read_csv('../Clean_Data/5-3.Combined_zillow_data_with_growthrate.csv',sep=',', encoding='latin-1')

##Getting City Averages for Columns
zillow_gb=zillow.groupby('City').mean()

##Changing data types so they are more  readable 
zillow_gb.zestimate=zillow_gb.zestimate.astype('long')
zillow_gb.valuation_high=zillow_gb.valuation_high.astype('long')
zillow_gb.valuation_low=zillow_gb.valuation_low.astype('long')
zillow_gb['tax assessment']=zillow_gb['tax assessment'].astype('long')
zillow_gb['tax assess year']=zillow_gb['tax assess year'].astype('int')
zillow_gb['lot size']=zillow_gb['lot size'].astype('long')
zillow_gb['finished sq ft']=zillow_gb['finished sq ft'].astype('long')
zillow_gb['year built']=zillow_gb['year built'].astype('long')
zillow_gb.bedrooms=zillow_gb.bedrooms.astype('int')
zillow_gb.bathrooms=zillow_gb.bathrooms.astype('int')

zillow_gb_lat_lng=[['latitude','longitude']]

##Deleting unnecessary columns
del zillow_gb['zpid']
del zillow_gb['latitude']
del zillow_gb['longitude']
del zillow_gb['message_code']

##Calculating some new measures
#Price per Lot Size
zillow_gb['PP_lot']=zillow_gb.zestimate/zillow_gb['lot size']
zillow_gb.PP_lot=zillow_gb.PP_lot.astype('int')
#Price per house size
zillow_gb['PP_sqft']=zillow_gb.zestimate/zillow_gb['finished sq ft']
zillow_gb.PP_sqft=zillow_gb.PP_sqft.astype('int')
zillow_gb

##Getting city house prices for box and whisker plots 
zillow_box=zillow[['City','zestimate']]

##Getting city house prices for box and whisker plots 
Glendale=zillow_box[zillow_box['City']=='Glendale']     
Burbank=zillow_box[zillow_box['City']=='Burbank'] 
Inglewood=zillow_box[zillow_box['City']=='Inglewood'] 
Alhambra=zillow_box[zillow_box['City']=='Alhambra'] 
Pasadena=zillow_box[zillow_box['City']=='Pasadena'] 
Long_Beach=zillow_box[zillow_box['City']=='Long Beach'] 
Los_Angeles=zillow_box[zillow_box['City']=='Los Angeles'] 
Palmdale=zillow_box[zillow_box['City']=='Palmdale'] 
Santa_Clarita=zillow_box[zillow_box['City']=='Santa Clarita'] 
Torrance=zillow_box[zillow_box['City']=='Torrance'] 

##Getting city house prices for box and whisker plots 
##Getting only 50 per city the cities dont have matching records 
Glendale=Glendale.sample(n=50)
Burbank=Burbank.sample(n=50)
Inglewood=Inglewood.sample(n=50)
Alhambra=Alhambra.sample(n=50)
Pasadena=Pasadena.sample(n=50)
Long_Beach=Long_Beach.sample(n=50)
Los_Angeles=Los_Angeles.sample(n=50)
Palmdale=Palmdale.sample(n=50)
Santa_Clarita=Santa_Clarita.sample(n=50)
Torrance=Torrance.sample(n=50)

##Getting city house prices for box and whisker plots 
Glendale.columns=['city','Glendal']
Burbank.columns=['city','Burbank']
Inglewood.columns=['city','Inglewood']
Alhambra.columns=['city','Alhambra']
Pasadena.columns=['city','Pasadena']
Long_Beach.columns=['city','Long_Beach']
Los_Angeles.columns=['city','Los_Angeles']
Palmdale.columns=['city','Palmdale']
Santa_Clarita.columns=['city','Santa_Clarita']
Torrance.columns=['city','Torrance']

##Getting city house prices for box and whisker plots 
Glendale=Glendale.reset_index()
Burbank=Burbank.reset_index()
Inglewood=Inglewood.reset_index()
Alhambra=Alhambra.reset_index()
Pasadena=Pasadena.reset_index()
Long_Beach=Long_Beach.reset_index()
Los_Angeles=Los_Angeles.reset_index()
Palmdale=Palmdale.reset_index()
Santa_Clarita=Santa_Clarita.reset_index()
Torrance=Torrance.reset_index()

##Getting city house prices for box and whisker plots 
df=pd.concat([Glendale.Glendal
           ,Burbank.Burbank
           ,Inglewood.Inglewood
           ,Alhambra.Alhambra
           ,Pasadena.Pasadena
           ,Long_Beach.Long_Beach
           ,Los_Angeles.Los_Angeles
           ,Palmdale.Palmdale
           ,Santa_Clarita.Santa_Clarita
           ,Torrance.Torrance],axis=1)
           
##Drawing the box and whisker plots to see the variances in terms of prices 
import seaborn as sns
from matplotlib import pyplot as plt
plt.figure(figsize=(10,6))
sns.boxplot(data=df)
plt.ylim(0,5000000)
plt.ylabel("Price, USD")
plt.title('House Price Ranges per City')
plt.xticks(rotation=45)
plt.savefig("../Clean_Data/6-2.House_Price_Ranges_per_City.png")
plt.show()

# Drawing out Average Price Per sqft per City
# set the plot x_axis, y_axis, title and label 
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x=zillow_gb.index, y="PP_sqft", data=zillow_gb, palette=sns.color_palette("Set3", 19))
plt.xticks(rotation=45)
plt.ylabel("Price, USD")
plt.title("Average Price Per Squarefeet Per City")
plt.savefig("../Clean_Data/6-2.Average_Price_Per_Squarefeet_Per_City.png")
plt.show()

# Drawing out Average Price Per lot per City
# set the plot x_axis, y_axis, title and label 
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x=zillow_gb.index, y="PP_lot", data=zillow_gb, palette=sns.color_palette("Set3", 19))
plt.xticks(rotation=45)
plt.ylabel("Price, USD")
plt.title("Average Price Per lot Per City")
plt.savefig("../Clean_Data/6-2.Average_Price_Per_lot_Per_City.png")
plt.show()

# Drawing out Average year built per City
# set the plot x_axis, y_axis, title and label 
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x=zillow_gb.index, y="year built", data=zillow_gb, palette=sns.color_palette("Set3", 19))
plt.xticks(rotation=45)
plt.ylim(1920,1990)
plt.ylabel("Year")
plt.title("Average year built Per City")

plt.savefig("../Clean_Data/6-2.Average_year_built_Per_City.png")
plt.show()


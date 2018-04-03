# Dependencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns, numpy as np
from itertools import cycle, islice

# File to load
fdata="../Clean_Data/5-2.Combined_zillow_data.csv"

# Read the Data
f_data=pd.read_csv(fdata, encoding = "ISO-8859-1")
f_data = f_data[["zpid", "address","city_state_zip","latitude","longitude","message_code","zestimate",
                 "rentzestimate","valuation_high","valuation_low",'valuechange',"home value index","tax assessment",
                 "tax assess year","year built","lot size","finished sq ft","bedrooms","bathrooms"]]
f_data.head()

# Using 30day value change to estimate full year growth rate
f_data['Housing Growth'] = f_data['valuechange']*12 / f_data['zestimate']
f_data.head()

# Get city data from city_state_zip
f_data['City'] = f_data.city_state_zip.str.split('\s+').str[1]
f_data = f_data.replace({"City": {'Los' : 'Los Angeles', 'Long' : 'Long Beach', 'Santa' : 'Santa Clarita', 'South':'Pasadena' }}) 
f_data['City'].value_counts()

# save file with estimate growth rate
f_data.to_csv(f'../Clean_Data/5-3.Combined_zillow_data_with_growthrate.csv')

# group data by city and find the average housing growth for each cuty
housing_growth_df = f_data.groupby(["City"])['Housing Growth'].agg(['mean']).sort_index().reset_index()
housing_growth_df = housing_growth_df.rename(columns={"mean":"Housing_Growth_Avg"})

# set the plot x_axis, y_axis, title and label 
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x="City", y="Housing_Growth_Avg", data=housing_growth_df, palette=sns.color_palette("Set3", 19))
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Percent of 1 Year Housing Growth(%)")
plt.title("1-Year Average Housing Growth Rate by City")

# Save the figure
plt.savefig("../Clean_Data/6-1.Ave_Housing_Growth_by_City.png")
plt.show()

# group data by city and find the average housing growth for each cuty
rent_price_df = f_data.groupby(["City"])["rentzestimate"].agg(['mean']).sort_index().reset_index()
rent_price_df = rent_price_df.rename(columns={"mean":"Rent_Price_Avg"})

# set the plot x_axis, y_axis, title and label 
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x="City", y="Rent_Price_Avg", data=rent_price_df, palette=sns.color_palette("Set3", 19))
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Average Rent Price")
plt.title("Average Rent Price by City")

# Save the figure
plt.savefig("../Clean_Data/6-1.Ave_Rent_Price_by-City.png")
plt.show()

# group data by city and find the average housing growth for each cuty
price_df = f_data.groupby(["City"])["zestimate"].agg(['mean']).sort_index().reset_index()
price_df = price_df.rename(columns={"mean":"House_Price_Avg"})

# set the plot x_axis, y_axis, title and label 
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x="City", y="House_Price_Avg", data=price_df, palette=sns.color_palette("Set3", 19))
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Average House Price")
plt.title("Average House Price by City")

# Save the figure
plt.savefig("../Clean_Data/6-1.Ave_House_Price_by_City.png")
plt.show()


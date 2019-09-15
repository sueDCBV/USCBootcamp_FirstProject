
# coding: utf-8

# In[2]:


#Using Census API to obtain information of interest to choose a city when buying a property
# code by Sue Del Carpio Bellido Vargas

# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

# please download census wrapper from https://pypi.python.org/pypi/census
from census import Census
import seaborn as sns

# Census API Key
from config import api_key

c = Census(api_key, year=2016)


# In[3]:


zipcodes_df = pd.read_csv("../Raw_Data/1-2.zipcodes_in_LA_counties.csv")

zipcodes_df = zipcodes_df.rename(columns={"zip": "Zipcode","County":"City"})

zipcodes_df.head()


# In[5]:


#Filter only selected cities for analysis
selected_cities=['Alhambra','Burbank','Inglewood','Glendale','Long Beach','Los Angeles','Palmdale','Pasadena','Santa Clarita','Torrance']
zipcodes_df=zipcodes_df[zipcodes_df['City'].isin(selected_cities)]
zipcodes_df.head()


# In[6]:


##Due to Timeout error, we need to call the API 3 times to obtain all information required

census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E","B19301_001E","B17001_002E",
                            "B23025_004E","B23025_002E","B23025_005E"),{'for': 'zip code tabulation area:*'})

census_pd = pd.DataFrame(census_data)

census_pd = census_pd.rename(columns={"B01003_001E": "Population",
                                      "B01002_001E": "Median Age",
                                      "B19013_001E": "Household Income",
                                      "B19301_001E": "Per Capita Income",
                                      "B17001_002E": "Poverty Count",
                                      "B23025_004E": "employment_employed",
                                      "B23025_002E": "Labor_force",
                                      "B23025_005E": "employment_unemployed",
                                      "NAME": "Name", "zip code tabulation area": "Zipcode"})

# Add in Poverty Rate (Poverty Count / Population)
census_pd["Poverty Rate"] = 100 *     census_pd["Poverty Count"].astype(
        int) / census_pd["Population"].astype(int)

# Add in Poverty Rate (Poverty Count / Population)
census_pd["Employment Rate"] = 100 *     census_pd["employment_employed"].astype(
        int) / census_pd["Labor_force"].astype(int)
    
# Add in Poverty Rate (Poverty Count / Population)
census_pd["Unemployment Rate"] = 100 *     census_pd["employment_unemployed"].astype(
        int) / census_pd["Labor_force"].astype(int)
    
#Final DataFrame
census_pd = census_pd[["Zipcode", "Population", "Median Age", "Household Income",
                       "Per Capita Income", "Poverty Count", "Poverty Rate","employment_employed","Labor_force","employment_unemployed",
                      "Employment Rate", "Unemployment Rate"]]

# Visualize
print(len(census_pd))
census_pd.head()


# In[7]:


census_data_2 = c.acs5.get(("NAME", "B01002_002E", "B01002_003E", "B08136_011E","B15003_002E","B01001_002E",
                            "B01001_026E"),{'for': 'zip code tabulation area:*'})

census_pd_2 = pd.DataFrame(census_data_2)

census_pd_2 = census_pd_2.rename(columns={"B01002_002E": "Median_male_age",
                                      "B01002_003E": "Median_female_age",
                                      "B08136_011E": "Walkable_time_min", 
                                      "B15003_002E": "Education_none",
                                      "B01001_002E": "Male_population",
                                      "B01001_026E": "Female_population",
                                      "NAME": "Name", "zip code tabulation area": "Zipcode"})

#Final DataFrame
census_pd_2 = census_pd_2[["Zipcode", "Median_male_age", "Median_female_age", "Walkable_time_min","Education_none", 
                           "Male_population", "Female_population"]]

# Visualize
print(len(census_pd_2))
census_pd_2.head()


# In[8]:


census_data_3 = c.acs5.get(("NAME", "B14002_001E", "B16003_002E", "B16003_008E","B19083_001E"),{'for': 'zip code tabulation area:*'})

# Convert to DataFrame
census_pd_3 = pd.DataFrame(census_data_3)

# Column Reordering
census_pd_3 = census_pd_3.rename(columns={"B14002_001E": "Students_population",
                                       "B16003_002E": "Population_from_5_17",
                                       "B16003_008E": "Population_18_over",
                                       "B19083_001E": "Gini_index",
                                      "NAME": "Name", "zip code tabulation area": "Zipcode"})
    
#Final DataFrame
census_pd_3 = census_pd_3[["Zipcode", "Students_population", "Population_from_5_17", "Population_18_over","Gini_index"]]
                        
# Visualize
print(len(census_pd_3))
census_pd_3.head()


# In[9]:


# Merge two dataframes using an inner join
merge_table_1 = pd.merge(census_pd, census_pd_2, on="Zipcode")
merge_table_1.head()
print(len(merge_table_1))


# In[10]:


# Merge two dataframes using an inner join
merge_table_total = pd.merge(merge_table_1, census_pd_3, on="Zipcode")
merge_table_total.head()
#print(len(merge_table_total))


# In[11]:


#Export clean data
merge_table_total.to_csv("../Clean_Data/3.total_census.csv", encoding="utf-8", index=False, header=True)


# # Cleaning Data

# In[12]:


#Get only Zipcodes from LA selected cities
import numpy as np
merge_table_total['Zipcode']=merge_table_total['Zipcode'].astype(np.int64)

los_angeles_census_df = pd.merge(merge_table_total, zipcodes_df, on="Zipcode")
los_angeles_census_df.to_csv("../Clean_data/3.los_angeles_census.csv", encoding="utf-8", index=False, header=True)


# In[13]:


los_angeles_census_df.columns


# In[14]:


# Dropping results with population=0
population_greater_0 = los_angeles_census_df["Population"]>0
los_angeles_census_df=los_angeles_census_df[population_greater_0]


# In[15]:


##We found default value in census is "-666666666"
##We are going to filter this data for each analysis


#Group by City, aggregation average by Gini index
gini_index_value = los_angeles_census_df["Gini_index"]>-666666666
gini_index_df = los_angeles_census_df[gini_index_value]

gini_index_df = gini_index_df.groupby(["City"])['Gini_index'].agg(['mean']).sort_index().reset_index()
gini_index_df= gini_index_df.rename(columns={"mean":"Gini_index_avg"})

gini_index_df=gini_index_df.sort_values(by='Gini_index_avg', ascending=False)
gini_index_df


# In[17]:


#Plot with seaborn, make additional changes with matplotlib
#Palette color reflects values from negative to positive for better understand

sns.set_style("whitegrid")
plt.figure(figsize=(15,7))
sns.barplot(x="City", y="Gini_index_avg", data=gini_index_df, palette=sns.color_palette("RdYlGn", 10))

plt.xlabel("")
plt.ylabel("Gini index")
plt.title("Household income distribution (Gini Coefficient)")

plt.show()

# Save the figure
plt.savefig("../Clean_Data/3.Gini_index_by_City.png")


# # UNEMPLOYMENT AND POVERTY ANALYSIS 

# In[18]:


##Clean and preparing data
unemployment_value = los_angeles_census_df["Unemployment Rate"]>-666666666
poverty_value = los_angeles_census_df["Poverty Rate"]>-666666666

poverty_unemployment_df = los_angeles_census_df[unemployment_value & poverty_value]

poverty_unemployment_df = poverty_unemployment_df.groupby(["City"])[['Unemployment Rate','Poverty Rate']].agg(['mean']).sort_index().reset_index()

poverty_unemployment_df.columns = poverty_unemployment_df.columns.droplevel(1)

poverty_unemployment_df= poverty_unemployment_df.rename(columns={"Unemployment Rate":"Unemployment_Rate","Poverty Rate":"Poverty_Rate"})

poverty_unemployment_df


# In[19]:


#Plot unemployment rate and poverty rate in two columns to compare results

sns.set()
poverty_unemployment_df = poverty_unemployment_df.set_index('City')

fig = plt.figure(figsize=(15,8)) # Create matplotlib figure

ax = fig.add_subplot(111) # Create matplotlib axes
ax2 = ax.twinx() # Create another axes that shares the same x-axis as a
width = .3

poverty_unemployment_df.Poverty_Rate.plot(kind='bar',color='blue', ax=ax2,width = width,position=0)

poverty_unemployment_df.Unemployment_Rate.plot(kind='bar',color='green',ax=ax,width=width, position=1)
ax.grid(None, axis=1)
ax2.grid(None)

ax.set_ylabel('Unemployment Rate')
ax2.set_ylabel('Poverty Rate')
plt.title("Unemployment and Poverty rate by Cities")
# Save the figure
plt.savefig("../Clean_Data/3.Unemployment_Poverty_rate_by_City.png")


# # WALKABLE ANALYSIS

# In[20]:


##Clean and preparing data
walk_time_value = los_angeles_census_df["Walkable_time_min"]>-666666666
walk_time_value_df = los_angeles_census_df[walk_time_value]

walk_time_value_df = walk_time_value_df.groupby(["City"])['Walkable_time_min'].agg(['sum']).sort_index().reset_index()
walk_time_value_df= walk_time_value_df.rename(columns={"sum":"Walkable_time_min_total"})

walk_time_value_df=walk_time_value_df.sort_values(by='Walkable_time_min_total', ascending=True)
walk_time_value_df


# In[21]:


sns.set_style("whitegrid")
plt.figure(figsize=(15,7))
sns.barplot(x="City", y="Walkable_time_min_total", data=walk_time_value_df, palette=sns.color_palette("RdYlGn", 10))

plt.xlabel("")
plt.ylabel("Walk time (min)")
plt.title("Walkable cities in LA County")

# Save the figure
plt.savefig("../Clean_Data/3.Walk_time_by_City.png")


# In[22]:


##Same analysis, without LA
selected_cities_no_la=['Alhambra','Burbank','Inglewood','Glendale','Long Beach','Palmdale','Pasadena','Santa Clarita','Torrance']
walk_time_value_no_la_df=walk_time_value_df[walk_time_value_df['City'].isin(selected_cities_no_la)]
walk_time_value_no_la_df

sns.set_style("whitegrid")
plt.figure(figsize=(15,7))
sns.barplot(x="City", y="Walkable_time_min_total", data=walk_time_value_no_la_df, palette=sns.color_palette("RdYlGn", 9))

plt.xlabel("")
plt.ylabel("Walk time (min)")
plt.title("Walkable cities without LA")

# Save the figure
plt.savefig("../Clean_Data/3.Walk_time_by_City_no_la.png")


# # AGE ANALYSIS

# In[23]:


##Clean and preparing data
median_age_value = los_angeles_census_df["Median Age"]>-666666666
median_male_age_value = los_angeles_census_df["Median_male_age"]>-666666666
median_female_age_value = los_angeles_census_df["Median_female_age"]>-666666666


age_stats_df = los_angeles_census_df[median_age_value & median_male_age_value & median_female_age_value]
age_stats_df = age_stats_df.groupby(["City"])[['Median Age','Median_male_age','Median_female_age']].agg(['mean']).sort_index().reset_index()
age_stats_df.columns = age_stats_df.columns.droplevel(1)
age_stats_df = age_stats_df.rename(columns={"Median Age":"Median_age"})

age_stats_df.head()


# In[24]:


##Unpivot data for Seaborn plots
sns.set_style("whitegrid")
age_stats_df_plot=age_stats_df[['City','Median_age','Median_male_age','Median_female_age']]

age_stats_df_upivot=pd.melt(age_stats_df_plot, id_vars=['City'], value_vars=['Median_age', 'Median_male_age','Median_female_age'])

cities=age_stats_df[['City']]

plt.figure(figsize=(28,10))
sns.barplot(x='City', y='value', hue='variable', data=age_stats_df_upivot)
plt.xticks(rotation=90)

plt.ylabel('age')
plt.title('Population Age by City')
plt.show()

# Save the figure
plt.savefig("../Clean_Data/3.Age_analysis_city.png")


# # EDUCATION ANALYSIS

# In[25]:


##Clean and preparing data
Education_none_value = los_angeles_census_df["Education_none"]>-666666666

education_df = los_angeles_census_df[Education_none_value]

education_df = education_df.groupby(["City"])[['Education_none','Population']].agg(['sum']).sort_index().reset_index()
education_df.columns = education_df.columns.droplevel(1)

# Add in Education none Rate (Education none Count / Population)
education_df["Education_none_Rate"] = 100 *     education_df["Education_none"].astype(
        int) / education_df["Population"].astype(int)
    
education_df=education_df.sort_values(by='Education_none_Rate', ascending=False)
education_df


# In[26]:


sns.set_style("whitegrid")
plt.figure(figsize=(15,7))
sns.barplot(x="City", y="Education_none_Rate", data=education_df, palette=sns.color_palette("RdYlGn", 10))

plt.xlabel("")
plt.ylabel("Education none rate")
plt.title("Education none rate by City")

# Save the figure
plt.savefig("../Clean_Data/3.Education_none_by_City.png")


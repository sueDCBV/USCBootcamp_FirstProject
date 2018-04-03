# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns

# Ranking is available through website: http://school-ratings.com/counties/Los_Angeles.html no API calls needed
school_csr_df = pd.read_csv("../Raw_Data/4.LA_cities_school_ranking.csv",encoding = "ISO-8859-1")
#zipcodes_df = zipcodes_df.rename(columns={"zip": "Zipcode","County":"City"})

school_csr_df.head()

#Filter only selected cities for analysis
selected_cities=['Alhambra','Burbank','Inglewood','Glendale','Long Beach','Los Angeles','Palmdale','Pasadena','Santa Clarita','Torrance']
school_csr_df=school_csr_df[school_csr_df['CITY'].isin(selected_cities)]
school_csr_df

#Group by City, aggregation average by Gini index

city_csr_df = school_csr_df.groupby(["CITY"])['CSR'].agg(['mean']).sort_index().reset_index()
city_csr_df= city_csr_df.rename(columns={"mean":"CSR_AVG"})

city_csr_df=city_csr_df.sort_values(by='CSR_AVG', ascending=True)
city_csr_df

sns.set_style("whitegrid")
plt.figure(figsize=(15,7))
sns.barplot(x="CITY", y="CSR_AVG", data=city_csr_df, palette=sns.color_palette("RdYlGn", 10))

plt.xlabel("")
plt.ylabel("CSR AVG")
plt.title("School Ranking by Cities in LA County")

# Save the figure
plt.savefig("../Clean_Data/4.School_Ranking_by_City.png")
plt.show()


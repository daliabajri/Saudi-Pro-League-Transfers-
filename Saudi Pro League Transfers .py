#!/usr/bin/env python
# coding: utf-8

#  ![OpenAI Logo](https://saudigazette.com.sa/uploads/images/2020/06/18/1584889.png)

# 
# <h1 align="center"> Saudi Pro League Transfers </h1>

# ### Importing Libararies and reading data

# In[37]:


import pandas as pd
import numpy as np

# For data cleaning
import re

# For visualization
import matplotlib.pyplot as plt 

# For correlation
import seaborn as sns


# In[2]:


# Reading file 

spl_transfers = pd.read_csv('saudi-pro-league-transfers.csv')

print(spl_transfers)


# In[3]:


#  displaying the fitst 10 row 

spl_transfers.head(10)


# In[4]:


spl_transfers.tail(10)


# In[5]:


spl_transfers.info()


# In[6]:


spl_transfers.columns #Displying columns names


# In[7]:


# Looking for clubs that had been repeated in the df
club_counts = spl_transfers['club_name'].value_counts()

print(club_counts)


# According to the data, the most frequent teams in transfers in the Saudi League Pro are Al-Ittihad Al-Ahly and Al-Nasr in first places, then followed by Al-Shabab, Al-Hilal and the rest of the other teams.

# ### Cleaning 'fee' column

# In[8]:


# 'Fee' column cleaning 

# By looking at the column data at the top, you can see that it contains a variety of data types

# Thus, we will use the unique function to find out the type of data, by creating new column 'Unique Fees'

unique_fees = pd.DataFrame(spl_transfers['fee'].unique(), columns=['Unique Fees'])

print(unique_fees)


# In[9]:


def clean_fee(fee):
    if pd.isnull(fee) or fee == '?' or fee == '-' or fee.startswith('End of loan'):
        return None
# Check if the fee value is null or contains '?' or '-' or starts with 'End of loan'. If any of these conditions are met, return None to represent a missing value.
   
    fee = str(fee)
    fee = fee.replace('€', '').replace('m', 'e6').replace('K', 'e3')
    
# Convert the fee value to a string and remove the '€' symbol. Replace 'm' with 'e6' to represent million and 'K' with 'e3' to represent thousand.    
    if re.match(r'^\d+\.?\d*e\d+$', fee):
        return float(fee)
    else:
        return None

# Check if the fee value matches the regular expression pattern for floating-point numbers. If it does, convert it to a float. Otherwise, return None.

spl_transfers['fee_cleaned'] = spl_transfers['fee'].apply(clean_fee)


# In[10]:


# Checking data after cleaning 'fee'

spl_transfers.head(10)


# In[11]:


spl_transfers.tail(10)


# ### The most expensive 20 deals in the Saudi League Pro

# In[12]:


# Assuming that the 'fee_cleaned' column that represents the cleaned fee amounts
# Convert the 'fee_cleaned' column to number in data type
spl_transfers['fee_cleaned'] = pd.to_numeric(spl_transfers['fee_cleaned'], errors='coerce')

# Sort the df by 'fee_cleaned' column in descending order
df_sorted = spl_transfers.sort_values('fee_cleaned', ascending=False)

# Get the top 20 deals
top_20_deals = df_sorted.head(20)





print('Top 20 Most Expinsive Deals in the Saudi Profissional league:')
print(top_20_deals)


# In[13]:


# Assuming that the 'fee_cleaned' column that represents the cleaned fee amounts
# Convert the 'fee_cleaned' column to number in data type
spl_transfers['fee_cleaned'] = pd.to_numeric(spl_transfers['fee_cleaned'], errors='coerce')

# Find the row with the highest fee amount 
highest_fee_row = spl_transfers.loc[spl_transfers['fee_cleaned'].idxmax()]

print('Highest Fee:')
print(highest_fee_row)


# The highest fee ever recorded in the Saudi Professional League occurred during the 2023/2024 season, involving Al-Hilal SFC and Paris SG. The transfer involved the renowned player Neymar, who joined Al-Hilal SFC as a left winger for a staggering fee of €90.00 million (€90,000,000).

# In[14]:


# Visualize the top 20 most expinsive deals


# Define the RGB values for the green color in the Saudi Arabian flag
green_color = (0/255, 155/255, 58/255)

plt.figure(figsize=(10, 6))
plt.bar(top_20_deals['player_name'], top_20_deals['fee_cleaned'], color=green_color)

plt.xlabel('Player Name')
plt.title('Top 20 Most Expensive Deals in the Saudi Profissional League')
plt.xticks(rotation=90)

plt.show()


# In[31]:


# Calulate the total deal amount for each club 
club_total = spl_transfers.groupby('club_name')['fee_cleaned'].sum()

# Select the top 5 clubs
top_5_clubs = club_total.nlargest(5)

top_5_clubs


# In[38]:


# Visulize the top 5 clubs

# create a pie chart
plt.figure(figsize=(8,8))
num_slices = len(top_5_clubs)
colors = plt.cm.get_cmap('Greens', num_slices)
plt.pie(top_5_clubs, labels=top_5_clubs.index, colors=colors(np.arange(num_slices)))
plt.title('Deals Distribution by Top 5 Clubs')
plt.show()


# Based on the information depicted in the pie chart, it is evident that the Al-hilal club has secured the highest-valued deals, accounting for the top three deals in terms of expense.
# 
# 

# ### Combine each club with the postion and extracting the number of deals and the average deal prices for each club and position

# In[15]:


# Group the data by club_name and postion, and calculate the number of deals and average deal prices
grouped_data = spl_transfers.groupby(['club_name', 'position']).agg({'fee_cleaned':['count', 'mean']})

# Flatten the column names
grouped_data.columns = ['num_deals', 'avg_deal_price']

# Reset the index to make 'club_name' and 'position' as regular columns
grouped_data = grouped_data.reset_index()

print('Number of deals and avgerage deal prices by club and position')
print(grouped_data)


# In[16]:


# Define the assessment criteria and corresponding symbols
assessment_criteria = [(0, 10, 'Low'), (10, 35, 'Mid')]

# Function to assign assessment values based on fee_cleaned price
def assign_transfer_rating(price):
    for lower, upper, rating in assessment_criteria:
        if lower <= price < upper:
            return rating
        return 'High'

# Create the 'transfer_rating' column by applying the assign_transfer_rating function to 'fee_cleaned'
spl_transfers['transfer_rating'] = spl_transfers['fee_cleaned'].apply(assign_transfer_rating)

spl_transfers


# In[17]:


# Define the bins and labels for the assessment categories
bins = [0, 1000000, 35000000, np.inf]
labels = ['Low', 'Mid', 'High']

# Create the 'transfer_rating' column using pandas.cut
spl_transfers['transfer_rating'] = pd.cut(spl_transfers['fee_cleaned'], bins=bins, labels=labels, right=False)

spl_transfers.head(20)


# In[18]:


# Extract the year from 'season' column and create the 'year' column
spl_transfers['year'] = spl_transfers['season'].str[:4]

spl_transfers


# In[19]:


# Calculate the total deal prices for each club
club_totals = spl_transfers.groupby('club_name')['fee_cleaned'].sum().reset_index()

# Sort the 'club_name' by the total deal price in descending order
club_total_sorted = club_totals.sort_values('fee_cleaned', ascending=False)

club_total_sorted


# In[20]:


# Visualize the total deal prices for each club
plt.figure(figsize=(10, 6))
plt.plot(club_total_sorted['club_name'], club_total_sorted['fee_cleaned'], marker='o', color=green_color)

plt.xlabel('Club')
plt.ylabel('Tota Deal Prices')
plt.title('Total Deal Prices by Club')
plt.xticks(rotation=90)

plt.show()


# From the graph, it is evident that the Al-Hilal team has secured the highest total deal prices in the Saudi Professional League, which amounts to 453,310,000 euros. There is a significant disparity between the deals of Al-Hilal and those of other clubs in terms of deal size.

# ## Correlation between Position and Deal prices

# In[21]:


# Calculate the average 'fee_cleaned' for each 'postion' categorey, since 'postion' is a categorical variable, we cannot directly calculate a correlation coefficient with 'fee_cleaned'.
# Calculating the average 'fee_cleaned' for each 'postion' categorey
position_avg_fee = spl_transfers.groupby('position')['fee_cleaned'].mean().reset_index()

# Create correlation matrix between 'position' and 'fee_cleaned'
corr_matrix = pd.pivot_table(position_avg_fee, values='fee_cleaned', index='position', columns='position')

# Create a heatmap to visualize the correlation matrix
plt.figure(figsize=(10,6))
sns.heatmap(corr_matrix, cmap='YlGnBu', annot=True, fmt='.2f', cbar=True)
plt.xlabel('Position')
plt.ylabel('Position')
plt.title('Heatmap: Average Fee Cleaned by Position')
plt.show()


# The heatmap illustrates that the position of Attacking Midfield has the highest average deal prices.

# In[22]:


corr_matrix.max()


# ## Total of deal prices for each year 

# In[23]:


#Calculate the total 'fee_cleaned' for each 'year'
yearly_total = spl_transfers.groupby('year')['fee_cleaned'].sum()


yearly_total


# In[24]:


# Create a bar plot
plt.figure(figsize=(10,6))
yearly_total.plot(kind='bar', color=green_color)
plt.xlabel=('Year')
plt.ylabel=('Total of Deal Prices')
plt.title=('Total of Deal Prices by Year')
plt.xticks(rotation=45)
plt.show()


# The bar graph highlights that the substantial player deal payments in 2023 have contributed to increased competitiveness within the SPL. As a result, the league has emerged as a formidable competitor to other prominent European leagues, such as the French, Spanish, and Italian leagues.

# Thank you
# 
# Dalia Bajriy

# In[ ]:





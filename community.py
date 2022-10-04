import pandas as pd
import csv

# Set your working directory
data = pd.read_csv("BU_Edge_Communities_report.csv")

#data['point_count'] = data['location'] + " " +  data['recording_date'] + " " +data['recording_time']

# dummies from the species code column, drops column
data['dummies'] = data['species_code']

abundance = pd.get_dummies(data=data, columns= ['dummies'], prefix='', prefix_sep='')

# add the species code column back
# df = pd.concat([data['species_code'], abundance], axis=1) 

with open('columnsList.csv', newline='') as f:
    reader = csv.reader(f)
    columnsList = list(reader)[0]

# make a dict of the aggregate function for each column. For the species code (length 4), use sum. Use first for the rest. Exclude 'location at indox 0.
columns_dictB =  { i : 'sum' for i in columnsList[1:] if len(i) == 4}
columns_dictA = { i : 'first' for i in columnsList[1:] if len(i) != 4}
columns_dictA.update(columns_dictB)
# Agg function for species_code is the list of all species counted at that location.
columns_dictA['species_code'] = lambda x: list(x)

# Use selcted columns only
df1 = abundance[columnsList]

# Group the report by unique location 
grouped = df1.groupby('location').agg(columns_dictA)

grouped.to_csv('community_abundance_by_location.csv')

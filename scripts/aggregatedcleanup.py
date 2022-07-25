# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 08:32:26 2022

@author: MayeKaypounyers
"""

import pandas as pd

aggdata = pd.read_csv("C:/Users/MayeKaypounyers/Downloads/ramp_utilities-main/ramp_utilities-main/ir_data_subsets/montana_state_university_RAMP_data.csv")
aggdata.head()
aggdata.info()
# records - 1048575

#Remove non-citable conent
aggdata = aggdata[aggdata.citableContent != "No"]
aggdata.head()
aggdata.info()
#records - 810885

#Remove no click data
aggdata = aggdata[aggdata.clicks != 0]
aggdata.head()
aggdata.info()


#Remove NA values
aggdata=aggdata.dropna()    
aggdata.head()
aggdata.info()
# records - 810828

#Sort based on unique_item_uri
aggdata = aggdata.sort_values(by="unique_item_uri")
aggdata.head()
aggdata.info()

# Delete date, url, citableContent, and index columns
aggdata = aggdata.drop(["date", "url", "citableContent","index"] , axis = 1)
aggdata.info()


# Create buckets for position
aggdata["position_bin"] = pd.cut(x=aggdata["position"], bins = [0,50,100,150,200,250,300,350,400,450,500])
aggdata.head(20)

for x in aggdata["position_bin"]:  
    aggdata[str(x)] = 0

#finish logic for column addition
for x in aggdata["position"]: 
    if x < 50.0:
        aggdata["columnrange1"] += 1
        aggdata ["columnrange2"] += 1
    
aggdata.head(20)
aggdata.info()

#Incrementing
z = 0
for n in range(10):
    z += 1
print(z)


#Save to csv for analysis
aggdata.to_csv("cleanaggdata")


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
aggdata.info()
aggdata.head()

#finish logic for column addition
 for x in aggdata["position"]: 
        if int(x) in range(0,51):
            aggdata["(0, 50]"] = 1
        elif int(x) in range(51,101):
            aggdata ["(50, 100]"] = 1
        elif int(x) in range(101,151):
            aggdata["(100, 150]"] = 1
        elif int(x) in range(151,201):
           aggdata["(150, 200]"] = 1
        elif int(x) in range (201,251):
            aggdata["(200, 250]"] = 1
        elif int(x) in range (251,301):
            aggdata["(250, 300]"] = 1
        elif int(x) in range (301, 351):
            aggdata["(300, 350]"] = 1
        elif int(x) in range (351,401):
            aggdata["(350, 400]"] = 1
        elif int(x) in range (401,451):
            aggdata["(400,450"] = 1
        elif int(x) in range (451,501):
            aggdata["(450, 500]"] = 1


     
aggdata["(0, 50]"].head(80)
aggdata.info()
aggdata.head()

#Incrementing
z = 0
for n in range(10):
    z += 1
print(z)


#Save to csv for analysis
aggdata.to_csv("cleanaggdata")


# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 08:32:26 2022

@author: MayeKaypounyers
"""

import pandas as pd

aggdata = pd.read_csv("../ir_data_subsets/montana_state_university_RAMP_data.csv")
aggdata.head()
aggdata.info()
# records - 1048575

#Remove non-citable conent
aggdata = aggdata[aggdata.citableContent == "Yes"].copy()
aggdata.head()
aggdata.info()
#records - 810885

#Remove no click data
aggdata = aggdata[aggdata.clicks > 0].copy()
aggdata.head()
aggdata.info()


#Remove NA values
aggdata=aggdata.dropna()    
aggdata.head()
aggdata.info()
# records - 810828

# group by unique_item_uri
print(len(pd.unique(aggdata["unique_item_uri"])))
aggGrouped = aggdata.groupby('unique_item_uri')
len(aggGrouped.groups)  # output should be the same as line 34

# let's work on a single group
print(aggGrouped.groups.keys())

one_item = aggGrouped.get_group('/1/10477')
print(one_item)

# get descriptive statistics
one_item.describe()

#Save to csv for analysis
aggdata.to_csv("cleanaggdata")


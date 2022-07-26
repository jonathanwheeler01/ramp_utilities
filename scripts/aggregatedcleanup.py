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

# view a single column
one_item["position"]

# aggregate some stats
item_clicks = one_item['clicks'].sum()
item_impressions = one_item['impressions'].sum()
item_clickthrough = item_clicks / item_impressions

# position categories
type(one_item)
for i, r in one_item.iterrows():
    serp_pos = r["position"]
    if serp_pos <= 10:
        print('p1')
    elif serp_pos > 10 and serp_pos <= 20:
        print('p2')
    elif serp_pos > 20 and serp_pos <=50:
        print("p3-p5")
    else:
        print('p6+')
        
# apply the above to an output
cols = ['repository_id', 'unique_item_uri', 
        'ct_serp_occurrences', 'sum_clicks',
        'sum_impressions', 'clickthrough_ratio',
        'mean_pos', 'median_pos', 'std_pos',
        'ct_pos_lte10', 'ct_pos_gt10_lte20',
        'ct_pos_gt20_lte50', 'ct_pos_gt50_lte100',
        'ct_pos_gt100']

out_df = pd.DataFrame(columns=cols)

repo_id = 'montana_state_university'
for name, group in aggGrouped:
    uid = name
    ct_serp = len(group)
    i_clicks = group['clicks'].sum()
    i_impressions = group['impressions'].sum()
    i_clickthrough = round(i_clicks / i_impressions, 3)
    mean_pos = group['position'].mean()
    med_pos = group['position'].median()
    std_pos = group['position'].std()
    p1 = 0
    p2 = 0
    p5 = 0
    p10 = 0
    p10plus = 0
    for p in group['position']:
        if p <= 10:
            p1 += 1
        elif p > 10 and p <= 20:
            p2 += 1
    
    


        
    

#Save to csv for analysis
aggdata.to_csv("cleanaggdata")


# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 08:32:26 2022

@author: MayeKaypounyers
"""

import pandas as pd

<<<<<<< Updated upstream
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

=======

import glob
files = glob.glob("./ir_data_subsets/*.csv")
print (files)

for file in files:
    ir = file
    
    #relative
    aggdata = pd.read_csv(ir)
    aggdata.head()
    aggdata.info()
    # records - 1048575
    
    #Remove non-citable conent
    aggdata = aggdata[aggdata.citableContent != "No"].copy()
    aggdata.head()
    aggdata.info()
    #records - 810885
    
    #Remove no click data
    aggdata = aggdata[aggdata.clicks != 0].copy()
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
    aggdata = aggdata.drop(["date", "url", "citableContent","index"] , axis = 1).copy()
    aggdata.info()
    
    
    print(len(pd.unique(aggdata["unique_item_uri"]))) #the number of unique uris
    aggGrouped = aggdata.groupby('unique_item_uri') #creates an object that stores the groups
    len(aggGrouped.groups) #length of groups in the object, counting each unique uri
    
    print(aggGrouped.groups.keys()) #retrieve the keys of the groups, the unique uri
    
    
    aggGrouped.head() #new dataframe object that is group and those groups can be operated on
    type(aggGrouped)
    
    print(aggGrouped.groups.keys())
    
    # =============================================================================
    # #one_item= aggGrouped.get_group('/1/9971')
    # print(one_item)
    # 
    # #descriptive stats for item
    # one_item.describe()
    # =============================================================================
    
    # #view one column of the group
    # one_item["position"]
    
    # #aggregate stats about items in the group
    # item_clicks = one_item['clicks'].sum()
    # item_impressions = one_item['impressions'].sum()
    # item_clickthrough = item_clicks / item_impressions
    # print(item_clicks)
    # print(item_impressions)
    # print(item_clickthrough)
    
    
    # type(one_item)
    # for i, r in one_item.iterrows():
    #     serp_pos = r["position"]
    #     if serp_pos <= 10:
    #         print('p1')
    #     elif serp_pos > 10 and serp_pos <= 20:
    #         print('p2')
    #     elif serp_pos > 20 and serp_pos <=50:
    #         print("p3-p5")
    #     else:
    #         print('p6+')
            
    cols = ['repository_id', 'unique_item_uri', 
            'ct_serp_occurrences', 'sum_clicks',
            'sum_impressions', 'clickthrough_ratio',
            'mean_pos', 'median_pos', 'std_pos',
            'ct_pos_lte10', 'ct_pos_gt10_lte20',
            'ct_pos_gt20_lte50', 'ct_pos_gt50_lte100',
            'ct_pos_gt100']
    
    out_df = pd.DataFrame(columns=cols)
    
    out_df.head()
    
    out_df = pd.DataFrame(columns=cols)
    
    repo_id = str(aggdata["repository_id"].unique())
    print(repo_id)
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
            elif p > 20 and p <= 50:
                p5 += 1
            elif p > 50 and p <= 100:
                p10 += 1
            else:
                p10plus += 1
        tdf = pd.DataFrame([[repo_id, uid, ct_serp, i_clicks,
                             i_impressions, i_clickthrough,
                             mean_pos, med_pos, std_pos,
                             p1, p2, p5, p10, p10plus]], columns=cols)
        out_df = pd.concat([out_df, tdf])
        
    out_df.info()
    out_df.head(30)
    
    out_df.to_csv("./aggregated_ir_subsets/" + repo_id +"grouped_logic.csv", index=False)
    
    
>>>>>>> Stashed changes

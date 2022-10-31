# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 08:32:26 2022

@author: MayeKaypounyers

This code iterates through the ir_subsets csv files to aggregate the files by unique_item_uri

"""

import glob
import pandas as pd
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
    
    
    print(len(pd.unique(aggdata["unique_item_uri"])))
    aggGrouped = aggdata.groupby('unique_item_uri') 
    len(aggGrouped.groups) 
    
    print(aggGrouped.groups.keys())
    
    
    aggGrouped.head() 
    type(aggGrouped)
    
    print(aggGrouped.groups.keys())
            
    cols = ['repository_id', 'unique_item_uri', 
             'sum_clicks',
            'sum_impressions', 'clickthrough_ratio',
            'mean_pos', 'median_pos',
            'ct_pos_lte10', 'ct_pos_gt10_lte20',
            'ct_pos_gt20_lte50', 'ct_pos_gt50_lte100',
            'ct_pos_gt100']
    
    out_df = pd.DataFrame(columns=cols)
    
    out_df.head()
    
    out_df = pd.DataFrame(columns=cols)
    
    repo_id = str(aggdata["repository_id"].unique()[0])
    print(repo_id)
    for name, group in aggGrouped:
        uid = name
        i_clicks = group['clicks'].sum()
        i_impressions = group['impressions'].sum()
        i_clickthrough = round(i_clicks / i_impressions, 3)
        mean_pos = group['position'].mean()
        med_pos = group['position'].median()
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
        tdf = pd.DataFrame([[repo_id, uid,  i_clicks,
                             i_impressions, i_clickthrough,
                             mean_pos, med_pos,
                             p1, p2, p5, p10, p10plus]], columns=cols)
        out_df = pd.concat([out_df, tdf])
        
    out_df.info()
    out_df.head(30)
    
    out_df.to_csv("./ir_subsets_itemagg/" + repo_id +"_grouped_logic_agg.csv", index=False) 
    

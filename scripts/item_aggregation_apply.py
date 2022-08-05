# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:49:26 2022

@author: MayeKaypounyers
"""

import pandas as pd

import glob
files = glob.glob("./ir_data_subsets/*.csv")
print (files)

for file in files: 
    ir = file

    aggdata = pd.read_csv(ir)
    #aggdata.head()
    #aggdata.info()
    # records - 1048575
    
    #Remove non-citable conent
    aggdata = aggdata[aggdata.citableContent == "Yes"].copy()
    #aggdata.head()
    #aggdata.info()
    #records - 810885
    
    #Remove no click data
    aggdata = aggdata[aggdata.clicks > 0].copy()
    #aggdata.head()
    #aggdata.info()
    
    
    #Remove NA values
    aggdata=aggdata.dropna()   
    #aggdata.head()
    #aggdata.info()
    # records - 810828
    
    
    
    def pos_buckets_per_row(pos_value):
        if pos_value <= 10:
            return 'lte10'
        elif pos_value > 10 and pos_value <= 20:
            return 'gt10_lte20'
        elif pos_value > 20 and pos_value <= 50:
            return 'gt20_lte50'
        elif pos_value > 50 and pos_value <= 100:
            return 'gt50_lte100'
        else:
            return 'gt100'
    
    aggdata['position_bucket'] = aggdata['position'].apply(pos_buckets_per_row)
    aggdata.info()
    aggdata[['position', 'position_bucket']].head()
    
    aggGrouped2 = aggdata.groupby('unique_item_uri')
    len(aggGrouped2.groups)
    
    # apply the above to an output
    cols = ['repository_id', 'unique_item_uri', 
            'ct_serp_occurrences', 'sum_clicks',
            'sum_impressions', 'clickthrough_ratio',
            'mean_pos', 'median_pos', 'std_pos',
            'ct_pos_lte10', 'ct_pos_gt10_lte20',
            'ct_pos_gt20_lte50', 'ct_pos_gt50_lte100',
            'ct_pos_gt100']
    
    out_df2 = pd.DataFrame(columns=cols)
    
    repo_id = aggdata["repository_id"].unique()
    for name, group in aggGrouped2:
        uid = name
        ct_serp = len(group)
        i_clicks = group['clicks'].sum()
        i_impressions = group['impressions'].sum()
        i_clickthrough = round(i_clicks / i_impressions, 3)
        mean_pos = group['position'].mean()
        med_pos = group['position'].median()
        std_pos = group['position'].std()
        p1 = len(group[group['position_bucket'] == 'lte10'])
        p2 = len(group[group['position_bucket'] == 'gt10_lte20'])
        p5 = len(group[group['position_bucket'] == 'gt20_lte50'])
        p10 = len(group[group['position_bucket'] == 'gt50_lte100'])
        p10plus = len(group[group['position_bucket'] == 'gt100'])
        tdf = pd.DataFrame([[repo_id, uid, ct_serp, i_clicks,
                             i_impressions, i_clickthrough,
                             mean_pos, med_pos, std_pos,
                             p1, p2, p5, p10, p10plus]], columns=cols)
        out_df2 = pd.concat([out_df2, tdf])
    
    out_df2.info()
    out_df2.head()
    
    out_df2.to_csv("./ir_subsets_itemagg/" + repo_id +"apply_logic_agg", index=False)

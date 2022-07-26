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
out_df.head()
    
# we could also try this using apply() on the cleaned dataframe
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

repo_id = 'montana_state_university'
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

out_df.to_csv("../ir_data_subsets/grouped_logic.csv", index=False)
out_df2.to_csv("../ir_data_subsets/apply_logic.csv", index=False)

aggdata[aggdata['position_bucket'] == 'gt10_lte20'].count()
len(aggdata[aggdata['position_bucket'] == 'gt10_lte20'])

#Save to csv for analysis
aggdata.to_csv("cleanaggdata")


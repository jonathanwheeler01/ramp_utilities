# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:47:40 2022

@author: MayeKaypounyers
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:01:24 2022

@author: jwheel01
"""

import pandas as pd


ir = 'montana_state_university'

# read item level ramp data
ramp_data = pd.read_csv('../ir_data_subsets/' + ir + '_RAMP_aggregated.csv')
ramp_data.info()

# read oaipmh metadata
oaipmh_meta = pd.read_csv('../ir_data_subsets/' + ir + '_oaipmh_metadata.csv')
oaipmh_meta.info()

# we need to join the dataframes using the oaipmh identifier of
# an item and its unique uid in the ramp data
# but these are not the same
ramp_data['unique_item_uri'].head()
oaipmh_meta['id'].head()

# we don't know without looking that a single approach will work
# for every IR, but MSU's case is not too difficult
# create a new field in the metadata dataframe to match the uid
oaipmh_meta['unique_item_uri'] = oaipmh_meta['id'].str.replace('oai:scholarworks.montana.edu:', '/')
oaipmh_meta['unique_item_uri'].head()
oaipmh_meta.head()

# get the metadata tags used
pd.unique(oaipmh_meta['tag'])

# subset to description
desc_meta = oaipmh_meta[oaipmh_meta['tag']== 'description'].copy()
desc_meta.info()
len(pd.unique(desc_meta['id']))
 # 8491

len(desc_meta)

# some items have more than one description field
# group by id to dig into this
desc_groups = desc_meta.groupby('id')
len(desc_groups.groups)

m_desc = []
for name, group in desc_groups:
    if len(group) > 1:
        m_desc.append(name)
        
len(m_desc)
8491 + 1647
# some items have more than 2 description fields...
# compare with abstract field
abs_meta = oaipmh_meta[oaipmh_meta['tag']== 'abstract'].copy()
len(pd.unique(abs_meta['id']))

# still duplicates...
# let's not join the dataframes
def get_item_desc_meta(unique_item_uri):
    item_meta = desc_meta[desc_meta['unique_item_uri'] == unique_item_uri].copy()
    desc_meta_values = item_meta['value']
    value_string = ";".join(desc_meta_values)
    return value_string

ramp_data['desc_meta'] = ramp_data['unique_item_uri'].apply(get_item_desc_meta)
    
ramp_data['desc_meta'].head()

ramp_data.info()

subject_meta = oaipmh_meta[oaipmh_meta['tag']== 'subject'].copy()

def get_item_subject_meta(unique_item_uri):
    item_meta = subject_meta[subject_meta['unique_item_uri'] == unique_item_uri].copy()
    subject_meta_values = item_meta['value']
    value_string = ";".join(subject_meta_values)
    return value_string

ramp_data['subject_meta'] = ramp_data['unique_item_uri'].apply(get_item_subject_meta)

ramp_data['subject_meta'].head()

ramp_data.info()

ramp_data.to_csv('../ir_data_subsets/' + ir + "_RAMP_desc_subject_meta.csv")



# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 10:57:55 2022

@author: MayeKaypounyers
"""

#%% Import libraries
# establish environment
import pandas as pd
import numpy as np
import glob
import os


#%% Import data
#import and structure SERP data
merged_serp_data = pd.read_csv("../merged_data/merged_ramp_all_features.csv")
merged_serp_data.drop(labels=["Unnamed: 0"], axis=1, inplace=True)
merged_serp_data.info()

#%% Add UID column
#create new column in SERP data
merged_serp_data['unique_id'] = merged_serp_data['repository_id'].map(str) + '-' + merged_serp_data['unique_item_uri'].map(str) 
merged_serp_data.info()


#%% Import clustered data
# Multiple files may exist from clustering different features
files = glob.glob("../serp_clustering_data/serp_clustered_data/*.csv")
print (files)

#%% Process data

# an alternative way to iterate through a collection of files
# without having to parse path/filename strings

for r, d, n in os.walk('../serp_clustering_data/serp_clustered_data/'):
    for name in n:
    
        #import and structure clustered data
        clustered_data = pd.read_csv(os.path.join(r, name))
        file_name = name
        print(file_name)
        
        
        #check uploaded data
        clustered_data.drop(labels=["Unnamed: 0"], axis=1, inplace=True)
        clustered_data.info()
        
        #create new columns in clustered data to match SERP data since some IDs are the same
        clustered_data['unique_id'] = clustered_data['repository_id'].map(str) + '-' + clustered_data['unique_item_uri'].map(str)
        clustered_data.info()
        
        
        #merge two feature dataset and serp data and remove additional columns
        clustered_and_serp = clustered_data.merge(merged_serp_data,on='unique_id')
        clustered_and_serp.drop(labels=["repository_id_y","unique_item_uri_y", 'unique_id'], axis=1, inplace=True)
        clustered_and_serp = clustered_and_serp.rename(columns = {'repository_id_x':'repository_id',"unique_item_uri_x":"unique_item_uri"})
        clustered_and_serp.info()
    
        
        
        #create groupby object to inspect clusters for two features
        groupby_summary = clustered_and_serp.groupby("serp_cluster")
        
        #items per cluster - two features
        groupby_summary.count() #13 may not be a good number in this case
        groupby_summary = groupby_summary.describe().reset_index()
        
        #save two feature summary dataset
        groupby_summary.to_csv('../serp_clustering_data/serp_cluster_summaries/' +name+".csv")

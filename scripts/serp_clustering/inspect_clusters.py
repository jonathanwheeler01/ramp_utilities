# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 10:57:55 2022

@author: MayeKaypounyers
"""


# establish environment
import pandas as pd
import numpy as np


#import and structure SERP data
merged_serp_data = pd.read_csv("./merged_data/merged_ramp_allfeatures.csv")
merged_serp_data.drop(labels=["Unnamed: 0"], axis=1, inplace=True)
merged_serp_data.info()

#create new column in SERP data
merged_serp_data['unique_id'] = merged_serp_data['repository_id'].map(str) + '-' + merged_serp_data['unique_item_uri'].map(str) 
merged_serp_data.info()

####################################### TWO FEATURES (CLICKS & ) ####################################

#import and structure clustered data
two_features_clustered = pd.read_csv("./clustering_and_scaling_data/twofeatures_clustered_data.csv")

#check uploaded data
two_features_clustered.drop(labels=["Unnamed: 0"], axis=1, inplace=True)
two_features_clustered.info()

#create new columns in clustered data to match SERP data since some IDs are the same
two_features_clustered['unique_id'] = two_features_clustered['repository_id'].map(str) + '-' + two_features_clustered['unique_item_uri'].map(str)
two_features_clustered.info()


#merge two feature dataset and serp data and remove additional columns
two_features_and_serp = two_features_clustered.merge(merged_serp_data,on='unique_id')
two_features_and_serp.drop(labels=["repository_id_y","unique_item_uri_y", 'unique_id'], axis=1, inplace=True)
two_features_and_serp = two_features_and_serp.rename(columns = {'repository_id_x':'repository_id',"unique_item_uri_x":"unique_item_uri"})
two_features_and_serp.info()


#save two feature dataset
two_features_and_serp.to_csv("./clustering_and_scaling_data/two_features_clustered_serp.csv", index = "unique_item_uri")


#create groupby object to inspect clusters for two features
two_features_summary = two_features_and_serp.groupby("serp_cluster_twofeatures")

#items per cluster - two features
two_features_summary.count() #13 may not be a good number in this case
two_features_summary = two_features_summary.describe().reset_index()

#save two feature summary dataset
two_features_summary.to_csv('./clustering_and_scaling_data/two_features_cluster_summary')

####################################### ALL FEATURES (CLICKS & ) ####################################

#import and structure clustered data
all_features_clustered = pd.read_csv("./clustering_and_scaling_data/allfeatures_clustered_data.csv")

#check uploaded data
all_features_clustered.drop(labels=["Unnamed: 0"], axis=1, inplace=True)
all_features_clustered.info()

#create new columns in clustered data to match SERP data since some IDs are the same
all_features_clustered['unique_id'] = all_features_clustered['repository_id'].map(str) + '-' + all_features_clustered['unique_item_uri'].map(str) 
all_features_clustered.info()

#merge all feature dataset and serp data and remove additional columns
all_features_and_serp = all_features_clustered.merge(merged_serp_data,on='unique_id')
all_features_and_serp.drop(labels=["repository_id_y","unique_item_uri_y", 'unique_id'], axis=1, inplace=True)
all_features_and_serp = all_features_and_serp.rename(columns = {'repository_id_x':'repository_id',"unique_item_uri_x":"unique_item_uri"})
all_features_and_serp.info()


#save all feature dataset
all_features_and_serp.to_csv( "./clustering_and_scaling_data/allfeatures_clustered_serp.csv", index = "unique_item_uri")

#items per cluster - all features
all_features_summary.count()
all_features_summary = all_features_summary.describe().reset_index()
all_features_summary.info()

#create groupby object to inspect clusters for all features
all_features_summary = all_features_and_serp.groupby('serp_cluster_allfeatures')

#save descriptive data about all features
all_features_summary.to_csv('./clustering_and_scaling_data/all_features_cluster_summary')

####################################### CLICKTHROUGHS  ####################################
#import and structure clustered data
clickthrough_clustered = pd.read_csv("./clustering_and_scaling_data/clickthrough_clusters.csv")

#check uploaded data
clickthrough_clustered.drop(labels=['Unnamed: 0'], axis=1, inplace=True)
clickthrough_clustered.info()

#create new columns in clustered data to match SERP data since some IDs are the same
clickthrough_clustered['unique_id'] = clickthrough_clustered['repository_id'].map(str) + '-' + two_features_clustered['unique_item_uri'].map(str)
clickthrough_clustered.info()


#merge all clickthrough clusters with SERP data
clickthrough_and_serp = clickthrough_clustered.merge(merged_serp_data, on = 'unique_id')
clickthrough_and_serp.drop(labels=["repository_id_y", "unique_item_uri_y","unique_id"], axis=1, inplace=True)
clickthrough_and_serp = clickthrough_and_serp.rename(columns = {'repository_id_x':'repository_id',"unique_item_uri_x":"unique_item_uri"})
clickthrough_and_serp.info()

#create groupby object to inspect clusters for clickthroughs
clickthrough_summary = clickthrough_and_serp.groupby('cluster')

#items per cluster - clickthrough
clickthrough_summary.count()
clickthrough_summary = clickthrough_summary.describe().reset_index()


#save descriptive data about two features 
clickthrough_summary.to_csv('./clustering_and_scaling_data/clickthrough_cluster_summary')

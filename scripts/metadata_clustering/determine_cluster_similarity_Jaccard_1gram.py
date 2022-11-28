# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:55:22 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd

#%% import subject metadata

subject_metadata = pd.read_csv('./metadata_clustering_data/subject_clustering/clean_subject_metadata.csv')

#%% import serp clusters

serp_clusters = pd.read_csv('./serp_clustering_data/serp_clustered_data/clickthrough_ratio.csv"')


#%%combine subject metadata and subject cluster data organized by cluster
subject_metadata.head()
subject_metadata.info()

#%%determine item similarity through one-hot encodings and Jaccard Similarity




#%% determine average similarity within clusters
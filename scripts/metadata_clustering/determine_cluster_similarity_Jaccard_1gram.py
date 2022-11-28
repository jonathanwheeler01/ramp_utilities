# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:55:22 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd

#%% import subject metadata
subject_metadata = pd.read_csv('./metadata_clustering_data/subject_clustering/clean_subject_metadata.csv')
del subject_metadata['Unnamed: 0']
subject_metadata.info()
#%% import serp clusters
serp_clusters = pd.read_csv('./serp_clustering_data/serp_clustered_data/clickthrough_ratio.csv')
del serp_clusters['Unnamed: 0']
serp_clusters.info()
#%%combine subject metadata and subject cluster data organized by cluster
subject_metadata['id'].head()
subject_metadata['unique_item_uri'] = subject_metadata['id'].str.split(':', expand=True)[2]
subject_metadata.head()
subject_metadata.info()

serp_clusters_and_metadata = pd.merge(serp_clusters, subject_metadata, on = "unique_item_uri", how = "inner")
#%%determine item similarity through one-hot encodings and Jaccard Similarity




#%% determine average similarity within clusters
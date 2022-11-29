# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:55:22 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd
import sqlite3

#%% import subject metadata
subject_metadata = pd.read_csv('./data/metadata_clustering_data/subject_clustering/clean_subject_metadata.csv')
del subject_metadata['Unnamed: 0']
subject_metadata.info()
subject_metadata.head()
#%% import serp clusters
serp_clusters = pd.read_csv('./data/serp_clustering_data/serp_clustered_data/clickthrough_ratio.csv')
del serp_clusters['Unnamed: 0']
serp_clusters.info()
serp_clusters.head()
#%%split id column in subject_metadata to get unique_item_uri
subject_metadata['id'].head()
subject_metadata['unique_item_uri'] = subject_metadata['id'].str.split(':', expand=True)[2]
subject_metadata['oairoot'] = subject_metadata['id'].str.split(':', expand=True)[1]
subject_metadata.head(3)
subject_metadata.info()

#remove id column
del subject_metadata['id']

#grab the repository name from database
con = sqlite3.connect("./metadata_database/metadata_database.db")
cur = con.cursor()
res = cur.execute("SELECT oairoot, repository_id  FROM repositories WHERE platform =  'dspace'")
res_list= []
res_list= res.fetchall()

#create a dataframe from the list of tuples
repo_df = pd.DataFrame(res_list, columns =['oairoot', 'repo_id'])

#use repo_df to add repo_id to subject_metadata
new_subject_metadata = pd.merge(subject_metadata, repo_df, on='oairoot', how='inner')
new_subject_metadata.head()

#create unique_id columns within both dataframes to merge
serp_clusters['unique_id'] = serp_clusters['repository_id'].map(str) + '-' + serp_clusters['unique_item_uri'].map(str) 
new_subject_metadata['unique_id'] = new_subject_metadata['repo_id'].map(str) + '-' +'/'+ new_subject_metadata['unique_item_uri'].map(str) 

#create combine dataframe
serp_clusters_and_metadata= pd.merge(serp_clusters, new_subject_metadata, on = "unique_id", how = "inner")

#remove additional columns
serp_clusters_and_metadata = serp_clusters_and_metadata[['unique_id', 'serp_cluster', 'clean_value']]

#organize by serp cluster
serp_clusters_and_metadata.sort_values(by=['serp_cluster'], inplace = True)

#%%determine item similarity through one-hot encodings and Jaccard Similarity




#%% determine average similarity within clusters
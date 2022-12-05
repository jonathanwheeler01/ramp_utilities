# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:38:17 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd
import sqlite3
import nltk
import nltk.cluster
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

#%% import subject metadata
subject_metadata = pd.read_csv('./data/metadata_clustering_data/subject_clustering/clean_subject_metadata.csv')
del subject_metadata['Unnamed: 0']
subject_metadata.info()
subject_metadata.head()
#%% import serp clusters
serp_clusters = pd.read_csv('./data/serp_clustering_data/serp_clustered_data/sum_clicks,sum_impressions.csv')
del serp_clusters['Unnamed: 0']
serp_clusters.info()
serp_clusters.head()
#%%combine and clean dataframes

#split id column in subject_metadata to get unique_item_uri
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

#create combined dataframe
serp_clusters_and_metadata= pd.merge(serp_clusters, new_subject_metadata, on = "unique_id", how = "inner")

#remove additional columns
serp_clusters_and_metadata = serp_clusters_and_metadata[['unique_id', 'serp_cluster', 'clean_value']]

#organize by serp cluster
serp_clusters_and_metadata.sort_values(by=['serp_cluster'], inplace = True)

#check data
serp_clusters_and_metadata.head()
serp_clusters_and_metadata.info()

#drop records without metadata
serp_clusters_and_metadata.dropna(subset=['clean_value'], inplace = True)
serp_clusters_and_metadata.info()

#%%divide the dataframe based on serp cluster

#could this be automated to base the cluster dataframes on the number of clusters 
cluster1= serp_clusters_and_metadata[serp_clusters_and_metadata['serp_cluster']==0]
cluster2= serp_clusters_and_metadata[serp_clusters_and_metadata['serp_cluster']==1]
cluster3= serp_clusters_and_metadata[serp_clusters_and_metadata['serp_cluster']==2]

#%%determine item similarity through one-hot encodings and cosine similarity
tfidf = TfidfVectorizer(stop_words='english', max_df=0.95, min_df= 10, max_features = 500)
data_bag = tfidf.fit_transform(serp_clusters_and_metadata['clean_value'])
feature_names = tfidf.get_feature_names()

#%% check top terms
sum_words = data_bag.sum(axis=0)

words_freq = [(word, sum_words[0, idx]) for word, idx in tfidf.vocabulary_.items()]
words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
frequency = pd.DataFrame(words_freq, columns=['word', 'freq'])

frequency.head(5).plot(x='word', y='freq', kind='bar', figsize=(15, 7))
plt.title("Most Frequently Occuring Words - Top 5")


#%% determine average similarity within clusters
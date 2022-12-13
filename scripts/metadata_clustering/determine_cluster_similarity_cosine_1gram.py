# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:38:17 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
#%%create column names variable to use later when saving file
print(serp_clusters.columns)

columns = input('Input name of columns used to cluster separated by commas: ')

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

print(cluster3)

#%%convert words to vectors for all clusters
countvector = CountVectorizer(stop_words='english', max_df=0.95, min_df= 5, max_features = 500)
data_bag = countvector.fit_transform(serp_clusters_and_metadata['clean_value'])
feature_names = countvector.get_feature_names()

print(countvector.vocabulary_)

#%%convert words to vectors for cluster 3
countvector3 = CountVectorizer(stop_words='english', max_df=0.95, min_df= 3, max_features = 500)
data_bag3 = countvector3.fit_transform(cluster3['clean_value'])
feature_names3 =countvector3.get_feature_names()
print(countvector3.vocabulary_)
print(data_bag3)

#%%convert vocabulary to dataframe for analysis
word_dataframe = pd.DataFrame(list(countvector3.vocabulary_.items()), columns = ['word', 'count'])

word_dataframe.head
#%% check top terms
#adjust for new vectorizer method
sum_words = data_bag3.sum(axis=0)


words_freq = [(word, sum_words[0, idx]) for word, idx in countvector3.vocabulary_]
words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
frequency = pd.DataFrame(words_freq, columns=['word', 'freq'])

frequency.head(5).plot(x='word', y='freq', kind='bar', figsize=(15, 7))
plt.title("Most Frequently Occuring Words (Cluster 3) - Top 5")


#%% cosine similarity for cluster 3

import pandas as pd

data_bag.toarray()

cluster3.info()

term_count_per_doc = pd.DataFrame(data_bag3.toarray(),columns = feature_names3 , index = cluster3['unique_id'])

similarity_matrix = cosine_similarity(term_count_per_doc,term_count_per_doc)

print(similarity_matrix)

type(similarity_matrix)

similarity_dataframe = pd.DataFrame(similarity_matrix, columns =list(cluster3['unique_id']), index=list(cluster3['unique_id']))

#%%store similarity dataframe

similarity_dataframe.to_csv('./data/metadata_clustering_data/subject_clustering/similarity_matrix_'+ columns +'.csv')
#%% Visualize the matrix with colored squares indicating similarity
fig = plt.figure(figsize=(8,8), dpi=300)
ax = fig.add_subplot(111)

ax.matshow(similarity_dataframe, cmap='Blues', vmin = 0.0, vmax = 0.2)


# Set the tick labels as the unique identifier
ax.set_xticklabels(list(similarity_dataframe.columns))
ax.set_yticklabels(list(similarity_dataframe.columns))

# Rotate the labels on the x-axis by 90 degrees
plt.xticks(rotation=90);

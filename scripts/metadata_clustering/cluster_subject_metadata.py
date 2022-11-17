# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:19:54 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

#%% import data
subject_metadata = pd.read_csv('./data/metadata_clustering_data/subject_clustering/clean_subject_metadata.csv')
#%% check data and remove extra column
subject_metadata.info()
del subject_metadata['Unnamed: 0']
subject_metadata.info()

#%% change column to string
subject_metadata['clean_value'] = subject_metadata.clean_value.astype(str)

#%%get tf-idf vectors from sklearn 

tfidf = TfidfVectorizer(stop_words='english', max_df=0.95, min_df= 10, max_features = 500)
data_bag = tfidf.fit_transform(subject_metadata['clean_value'])
feature_names = tfidf.get_feature_names()

#%% check features
feature_names[:10]

#%% check top terms
sum_words = data_bag.sum(axis=0)

words_freq = [(word, sum_words[0, idx]) for word, idx in tfidf.vocabulary_.items()]
words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
frequency = pd.DataFrame(words_freq, columns=['word', 'freq'])

frequency.head(20).plot(x='word', y='freq', kind='bar', figsize=(15, 7))
plt.title("Most Frequently Occuring Words - Top 20")

#%%check other features
frequency.tail(20).plot(x='word', y='freq', kind='bar', figsize=(15,7))
plt.title("Least Frequently Occuring Words - Bottom 20")

#%% determine appropriate clusters using the elbow method
inertias = []
Ks = []
for K in range(1,11):
    ## initialize the algorithm
    kmeans = KMeans(n_clusters=K)
    ## run the algorithm on the data
    kmeans.fit(data_bag)

    Ks.append(K)
    inertias.append(kmeans.inertia_)

  #%% cluster the data

from sklearn.cluster import KMeans

#how did I choose 5??
number_of_clusters=5
## complete the code

clusters = KMeans(n_clusters= number_of_clusters, max_iter = 1000)
clusters.fit(df_bag)
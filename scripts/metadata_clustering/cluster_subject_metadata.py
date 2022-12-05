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
#%% clean and restructure data
#check data remove extra column & items ids without metadata
subject_metadata.info()

# remove extra column
del subject_metadata['Unnamed: 0']
subject_metadata.info()

#remove ids without metadata
subject_metadata.dropna(subset=['clean_value'], inplace = True)
subject_metadata.info()

subject_metadata.set_index("id", inplace = True)
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

frequency.head(10).plot(x='word', y='freq', kind='bar', figsize=(15, 7))
plt.title("Most Frequently Occuring Words - Top 10")

#%%check bottom terms
frequency.tail(10).plot(x='word', y='freq', kind='bar', figsize=(15,7))
plt.title("Least Frequently Occuring Words - Bottom 10")

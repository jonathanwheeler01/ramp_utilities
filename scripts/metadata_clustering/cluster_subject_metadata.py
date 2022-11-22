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

frequency.head(20).plot(x='word', y='freq', kind='bar', figsize=(15, 7))
plt.title("Most Frequently Occuring Words - Top 20")

#%%check bottom terms
frequency.tail(20).plot(x='word', y='freq', kind='bar', figsize=(15,7))
plt.title("Least Frequently Occuring Words - Bottom 20")
#%% create function to initialize the algorithm and fit the data
inertias = []
Ks = []
for K in range(1,11):
    ## initialize the algorithm
    kmeans = KMeans(n_clusters=K)
    ## run the algorithm on the data
    kmeans.fit(data_bag)

    Ks.append(K)
    inertias.append(kmeans.inertia_)

## gather the best result
best_combined_score, best_K, best_inertia = min(zip([K*I for K, I in zip(Ks, inertias)], Ks, inertias))
print("best k of combined score: ", best_K)

## initialize a wide figure
fig = plt.figure(figsize = (12,6))

## plot the inertia vs cluster number
fig.add_axes([0,0,0.45,1])
_ = plt.plot(Ks, inertias, color = "black", linestyle = 'dashed')#ls =3
_ = plt.scatter(best_K, best_inertia, s = 50, color = "red")
_ = plt.xlabel("K", fontsize = 15)
_ = plt.ylabel("Inertia", fontsize = 15)

## plot the inertia times cluster number
fig.add_axes([0.55,0,0.5,1])
_ = plt.plot(Ks, [K*I for K, I in zip(Ks, inertias)], color = "black", linestyle = 'dashed')#ls = 3
_ = plt.scatter(best_K, best_combined_score, s = 50, color = "red")
_ = plt.xlabel(r"K", fontsize = 15)
_ = plt.ylabel(r"$k \times I$", fontsize = 15)

#%% Create K-Means Object 

clusters = KMeans(n_clusters= 5, max_iter = 1000)
clusters.fit(d)

results = pd.DataFrame({
    'text': subject_metadata['clean_value'],
    'category': clusters.labels_
})
results

#%%
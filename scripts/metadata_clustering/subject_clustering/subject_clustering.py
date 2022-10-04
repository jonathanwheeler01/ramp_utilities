# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:56:24 2022

@author: MayeKaypounyers
"""

#import libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

#import data
preproc_sub_terms = 

#clean data

#establish vectorizer

#print top terms per cluster
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print
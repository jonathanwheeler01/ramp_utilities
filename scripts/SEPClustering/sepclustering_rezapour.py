# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 14:00:49 2022

@author: MayeKaypounyers
"""
###################################################################  ENVIRONMENT PREP AND DATA CLEANING ###################################################################################

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
%matplotlib inline

#import data and set index column
X = pd.read_csv('C:/Users/MayeKaypounyers/Documents/GitHub/ramp_utilities/ir_subsets_itemagg/brock_universitygrouped_logic.csv')
X.set_index("unique_item_uri", inplace = True)

#check imported data
X.head()
X.shape
X.isnull().sum() #the algorithm does not accept the null/empty values

#remove standard deviation column since it contains blanks
del X['std_pos']
X.isnull().sum()
X.info()

##################################################################### SCALING THE DATA ####################################################################################

# define min max scaler
scaler = MinMaxScaler()

# transform data
X = scaler.fit_transform(X.to_numpy())
X = pd.DataFrame(X)
X.head()

########################################################## ELBOW METHOD FOR NUMBER OF K (FROM DR. REZAPOUR) ####################################################### 

#create function to initialize the algorithm and fit the data
inertias = []
Ks = []
for K in range(1,11):
    ## initialize the algorithm
    kmeans = KMeans(n_clusters=K)
    ## run the algorithm on the data
    kmeans.fit(X)

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


################################################################ CLUSTERING METHOD FROM DR. REZAPOUR ##################################################################################

## get kmeans clustering from sklearn
from sklearn.cluster import KMeans

## initialize the algorithm
kmeans = KMeans(n_clusters=4)

## run the algorithm on the data
kmeans.fit(X)

## gather the predicted cluster labels
y_hat = kmeans.predict(X)

## make empty lists for the predicted cluster centers
model_c_x = []
model_c_y = []

## loop through the clusters and find their centers -- 
for label in set(y_hat):
    model_c_x.append(np.mean(X[y_hat==label, 0])) ### Invalid Index Error
    model_c_y.append(np.mean(X[y_hat==label, 1]))
        
## initialize a wide figure
fig = plt.figure(figsize = (12,6))

## plot the original data and "true" centers
fig.add_axes([0,0,0.5,1])
_ = plt.scatter(X[:, 0], X[:, 1], s=50, c = y)
_ = plt.scatter(c_x, c_y, s=50, color = "blue")

## plot the modeled data and "predicted" centers
fig.add_axes([0.5,0,0.5,1])
_ = plt.scatter(X[:, 0], X[:, 1], s=50, c = y_hat)
_ = plt.scatter(model_c_x, model_c_y, s=50, color = "red")
_ = plt.scatter(c_x, c_y, s=50, color = "blue")

for label in set(y_hat):
    model_c_x.append(np.mean(X[y_hat==label, 0]))
    model_c_y.append(np.mean(X[y_hat==label, 1]))
        
## initialize a wide figure
fig = plt.figure(figsize = (12,6))

## plot the original data and "true" centers
fig.add_axes([0,0,0.5,1])
_ = plt.scatter(X[:, 0], X[:, 1], s=50, c = y)
_ = plt.scatter(c_x, c_y, s=50, color = "blue")

## plot the modeled data and "predicted" centers
fig.add_axes([0.5,0,0.5,1])
_ = plt.scatter(X[:, 0], X[:, 1], s=50, c = y_hat)
_ = plt.scatter(model_c_x, model_c_y, s=50, color = "red")
_ = plt.scatter(c_x, c_y, s=50, color = "blue")
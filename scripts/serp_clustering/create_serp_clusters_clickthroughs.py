# -*- coding: utf-8 -*-
"""
Spyder Editor

This script was created to determine item clusters based on RAMP provided Search Engine Results Page (SERP) data.
Features measured are:
    -Click-through Ratio
"""

########################################################### ENVIRONEMENT SETUP AND DATA IMPORT ###############################################################

#import required libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


# import glob
files = glob.glob("./ir_subsets_itemagg/*.csv")

#combine files
all_files = glob.glob("./ir_subsets_itemagg/*.csv")
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv( "./merged_data/merged_ramp_clickthrough.csv")


# Import data set 
df= pd.read_csv("./merged_data/merged_ramp_clickthrough.csv")

#check imported data
df.head()
df.info()
df.isnull().sum()

#remove remove blank columns and those not needed in the 2 feature analysis
df = df[["repository_id","unique_item_uri",'clickthrough_ratio']].copy()

#create a merged column based on repository id and unique item uri
df['unique_id'] = df['repository_id'].map(str) + '-' + df['unique_item_uri'].map(str) 
df.head()  

#set index as unique uri
df.set_index("unique_id", inplace = True)
df.info()

#remove unneccessary columns that were joined
df.drop(labels=["repository_id","unique_item_uri"], axis=1, inplace=True)
df.info()


############################################################ ELBOW METHOD FROM DR. REZAPOUR #####################################################################

#create function to initialize the algorithm and fit the data

inertias = []
Ks = []
for K in range(1,35):
    ## initialize the algorithm
    kmeans = KMeans(n_clusters=K)
    ## run the algorithm on the data
    kmeans.fit(df)

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


############################################################## K-MEANS FROM YOUTUBE ############################################################################
#Create K-Means Object 
kmeans = KMeans(n_clusters=5)

#fit the data to the model and apply the cluster numbers to the dataframe
df['cluster'] = kmeans.fit_predict(df)

df.head(20)
df.info()

#reset index
df.reset_index(inplace=True)

#Split unique id column
df[['repository_id','unique_item_uri']] = df['unique_id'].str.split("-", expand=True)
df.info()

#remove unique_id column
df.drop("unique_id",axis=1, inplace=True)
df.head()


#print data
df.to_csv( "./clustering_and_scaling_data/clickthrough_clusters.csv", index = "unique_item_uri")


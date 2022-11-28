# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:34:52 2022

@author: MayeKaypounyers
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This script was created to determine item clusters based on RAMP provided Search Engine Results Page (SERP)
Use the following list of column names to determine clustering features:
repository_id
unique_item_uri
sum_clicks
sum_impressions
clickthrough_ratio
mean_pos
median_pos
ct_pos_lte10
ct_pos_gt10_lte20
ct_pos_gt20_lte50
ct_pos_gt50_lte100
ct_pos_gt100

working directory:  ./serp_and_subject_clustering/data/
"""

#%% Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


#%% Read and combine files
all_files = glob.glob("./ir_subsets_itemagg/*.csv")
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv( "./merged_data/merged_ramp_all_features.csv")

#%% Import merged dataset
df= pd.read_csv("./merged_data/merged_ramp_all_features.csv")

#check imported data
df.info()

 #%% Create list of features
# what are the options?
for v in list(df.columns.values):
    print(v)
#input features to be clustered on; separated by commas, do not use spaces
# add a little space for data entry
columns =input("Features separated by commas: ")


#create list
columns_list = columns.split(",")
print(columns_list)

#%% Keep ID columns
id_columns = ['repository_id','unique_item_uri']

#%% Define column subset
#join with columns needed for identification
id_columns_list = columns_list + id_columns

#%% Subset to defined columns
df = df[id_columns_list].copy() 

#%% Create globally unique item ID
#create a merged column based on repository id and unique item uri
df['unique_id'] = df['repository_id'].map(str) + '-' + df['unique_item_uri'].map(str) 
df.head()  

#%% Set index on unique_id column
df.set_index("unique_id", inplace = True)
df.info()

#%% Drop previous ID columns
df.drop(labels=["repository_id","unique_item_uri"], axis=1, inplace=True)
df.info()
df.head()

#%% Coerce columns variable to str
columns = str(columns)

#%% Initialize a scaler
scaler = MinMaxScaler()

#%% Scale the data
df[:] = scaler.fit_transform(df)

#%% Save scaled data to file
#save scaled data
df.to_csv( "./serp_clustering_data/serp_scaled_data/"+columns+".csv")

#%% Elbow method
#create function to initialize the algorithm and fit the data
inertias = []
Ks = []
for K in range(1,10):
    ## initialize the algorithm
    kmeans = KMeans(n_clusters=K)
    ## run the algorithm on the data
    kmeans.fit(scaled_data)

    Ks.append(K)
    inertias.append(kmeans.inertia_)

# Gather the best result
best_combined_score, best_K, best_inertia = min(zip([K*I for K, I in zip(Ks, inertias)], Ks, inertias))
print("best k of combined score: ", best_K)

# Initialize figure
fig = plt.figure(figsize = (12,6))

# Plot inertia v cluster #

fig.add_axes([0,0,0.45,1])
_ = plt.plot(Ks, inertias, color = "black", linestyle = 'dashed')#ls =3
_ = plt.scatter(best_K, best_inertia, s = 50, color = "red")
_ = plt.xlabel("K", fontsize = 15)
_ = plt.ylabel("Inertia", fontsize = 15)

# Plot inertia * cluster #
fig.add_axes([0.55,0,0.5,1])
_ = plt.plot(Ks, [K*I for K, I in zip(Ks, inertias)], color = "black", linestyle = 'dashed')#ls = 3
_ = plt.scatter(best_K, best_combined_score, s = 50, color = "red")
_ = plt.xlabel(r"K", fontsize = 15)
_ = plt.ylabel(r"$k \times I$", fontsize = 15)


#%%  KMeans clustering
clusters = input("How many clusters would you like to create? ")

clusters =int(clusters)
kmeans = KMeans(n_clusters=clusters)


#%% Fit the data
kmeans.fit(df)

df['serp_cluster'] = kmeans.fit_predict(df)

#check scaled 
df.head(20)
df.info()


#%% Reset index
df.reset_index(inplace=True)

#%% Split unique_id column

df[['repository_id','unique_item_uri']] = df['unique_id'].str.split("-", expand=True)
df.info()

#%% Remove column
df.drop("unique_id",axis=1, inplace=True)
df.head()

#%% Rename dataset
clustered_data=df
clustered_data.head()
clustered_data.info()

#%% Output to CSV
clustered_data.to_csv( "./serp_clustering_data/serp_clustered_data/"+columns+".csv", index = "unique_item_uri")
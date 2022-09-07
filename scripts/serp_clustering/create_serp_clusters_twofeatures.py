# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:34:52 2022

@author: MayeKaypounyers
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This script was created to determine item clusters based on RAMP provided Search Engine Results Page (SERP) data.
Features measured are:
    - Sum of Item Clicks
    - Sum of Item Impressions
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
df_merged.to_csv( "./ir_subsets_itemagg/merged_ramp_twofeatures.csv")


# Import data set 
df= pd.read_csv("./ir_subsets_itemagg/merged_ramp_twofeatures.csv")

#check imported data
df.head()
df.info()
df.isnull().sum()

#remove remove blank columns and those not needed in the 2 feature analysis
df = df[["unique_item_uri",'sum_clicks','sum_impressions']].copy()


#set index as unique uri
df.set_index("unique_item_uri", inplace = True)
df.info()

################################################################# SCALING THE DATA #######################################################################

# define min max scaler
scaler = MinMaxScaler()

# transform data
scaled_data=  scaler.fit_transform(df)
scaled_data = pd.DataFrame(scaled_data)
scaled_data.head()
scaled_data.columns = df.columns
scaled_data.index = df.index #will this keep the index correct?

scaled_data.info()
df.info()
df.head(20)
scaled_data.head(20)

#save scaled data
scaled_data.to_csv( "./clustered_and_scaled_data/twofeatures_scaled_data.csv")
############################################################ ELBOW METHOD FROM DR. REZAPOUR #####################################################################

#create function to initialize the algorithm and fit the data
inertias = []
Ks = []
for K in range(1,11):
    ## initialize the algorithm
    kmeans = KMeans(n_clusters=K)
    ## run the algorithm on the data
    kmeans.fit(scaled_data)

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

#Code follows the last number in the K range (in this case K is equal to 10, but when 11 is changed to 15, K becomes 14)

############################################################## K-MEANS FROM YOUTUBE ############################################################################
#Create K-Means Object 
kmeans = KMeans(n_clusters=5)

#fit the data to the model and apply the cluster numbers to the dataframe
scaled_data['serp_cluster_twofeatures'] = kmeans.fit_predict(scaled_data)

scaled_data.head(20)
scaled_data.info()

#remove clicks and impressions data
scaled_data.drop(["sum_clicks","sum_impressions"], axis =1, inplace=True)


#check data frame
scaled_data.info()
scaled_data.head(20)

#reattach respository ID
lookup_table = pd.read_excel("./supplementary_data/uri_lookup.xlsx")
lookup_table.head()


clustered_data_uri= scaled_data.merge(lookup_table, on="unique_item_uri")
clustered_data_uri.head()


#print data
clustered_data_uri.to_csv( "./clustered_and_scaled_data/twofeatures_clustered__data.csv", index = "unique_item_uri")
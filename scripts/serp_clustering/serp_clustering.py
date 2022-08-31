# -*- coding: utf-8 -*-
"""
Spyder Editor

This script was created to determine item clusters based on RAMP provided Search Engine Results Page (SERP) data.
Features measured are:
    - Count of SERP occurences
    - Sum of Item Clicks
    - Sum of Item Impressions
    -Click-through Ratio
    - Count of  Page position less than or equal to 10
    - Count of Page position greater than 10 but less than or equal to 20
    - Count of Page position greater than 20 but less than or equal to 50
    - Count of Page position greater than 50 but less than or equal to 100
    - Count of Page position greater than 100
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
print (files)

#combine files
all_files = glob.glob("./ir_subsets_itemagg/*.csv")
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv( "./ir_subsets_itemagg/merged.csv")


# Import data set 
df= pd.read_csv("./ir_subsets_itemagg/merged.csv")

#check imported data
df.head()
df.info()
df.isnull().sum()

#remove standard deviation column since it contains blanks and added columns from import
#delete additional columns
df.drop(['std_pos',"Unnamed: 0","Unnamed: 0.1" , "mean_pos", "median_pos", "repository_id"], axis =1, inplace=True)

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
scaled_data.to_csv( "./clustering_data/scaled_data.csv")
############################################################ ELBOW METHOD FROM DR. REZAPOUR #####################################################################

#create function to initialize the algorithm and fit the data
inertias = []
Ks = []
for K in range(1,15):
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
scaled_data['sep_cluster'] = kmeans.fit_predict(scaled_data)

scaled_data.head(20)
scaled_data.info()

#check all clusters
scaled_data0 = scaled_data[scaled_data.cluster==0] 
scaled_data1 = scaled_data[scaled_data.cluster==1]
scaled_data2 = scaled_data[scaled_data.cluster==2]
scaled_data3= scaled_data[scaled_data.cluster==3]
scaled_data4 =scaled_data[scaled_data.cluster== 4]

print(scaled_data0)
print(scaled_data1)
print(scaled_data2)
print(scaled_data3)
print(scaled_data4)


#check data frame
scaled_data.info()
scaled_data.head(20)

#reattach respository ID
lookup_table = pd.read_excel("./supplementary_data/uri_lookup.xlsx")
lookup_table.head()


clustered_data_uri= scaled_data.merge(lookup_table, on="unique_item_uri")
clustered_data_uri.head()


#print data
clustered_data_uri.to_csv( "./clustering_data/clustered_scaled_data.csv", index = "unique_item_uri")

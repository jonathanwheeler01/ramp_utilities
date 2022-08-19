# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

############################################################ ELBOW METHOD FROM YOUTUBE #####################################################################

#Clustering the data

# test for kmeans clustering from YouTube

#import required libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Import data set 
df = pd.read_csv('C:/Users/MayeKaypounyers/Documents/GitHub/ramp_utilities/ir_subsets_itemagg/brock_universitygrouped_logic.csv')
df.set_index("unique_item_uri", inplace = True)

#check imported data
df.head()
df.shape
df.isnull().sum()

#remove standard deviation column since it contains blanks
del df['std_pos']
df.head()

# Collecting the distortions into list
distortions = []
K = range(1,10)
for k in K:
 kmeanModel = KMeans(n_clusters=k)
 kmeanModel.fit(df)
 distortions.append(kmeanModel.inertia_)
 
# Plotting the distortions
plt.figure(figsize=(16,8))
plt.plot(K, distortions,'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('Elbow Method')
plt.show()

################################################################# SCALING THE DATA #######################################################################

# # define min max scaler
# scaler = MinMaxScaler()

# # transform data
# X = scaler.fit_transform(X.to_numpy())
# X = pd.DataFrame(X)
# X.head()

############################################################## K-MEANS FROM YOUTUBE ############################################################################
#Create K-Means Object 
kmeans = KMeans(n_clusters=10)

#fit the data to the model and apply the cluster numbers to the dataframe
df['cluster'] = kmeans.fit_predict(df)

df0 = df[df.cluster==0] 
df1 = df[df.cluster==1]
df2 = df[df.cluster==2]
df3 =df[df.cluster==3]
print(df0)
print(df1)
print(df2)
print(df3)

#Assign the clusters to a variable
centers = kmeans.cluster_centers_

#print clusters
print(centers)

#converging the clusters
df['cluster'] = kmeans.fit_predict(df)
df['cluster'].unique()

df0 = df[df.cluster==0] 
df1 = df[df.cluster==1]
df2 = df[df.cluster==2]
df3 = df[df.cluster == 3]
df4 = df[df.cluster == 4]
df5 = df[df.cluster == 5]
df6 = df[df.cluster == 6]
df7 = df[df.cluster == 7]
df8 = df[df.cluster == 8]
df9 = df[df.cluster == 9]
df10 = df[df.cluster == 10]

df0.head()
df1.head()
df2.head()
df3.head()
# df4.head()
# df5.head()

#how do I bring back the index number?
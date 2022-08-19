# -*- coding: utf-8 -*-
"""
Spyder Editor

Youtube Script
"""

########################################################### ENVIRONEMENT SETUP AND DATA IMPORT ###############################################################
#import required libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Import data set 
df= pd.read_csv('C:/Users/MayeKaypounyers/Documents/GitHub/ramp_utilities/ir_subsets_itemagg/brock_universitygrouped_logic.csv')
df.set_index("unique_item_uri", inplace = True)

#check imported data
df.head()
df.info()
df.isnull().sum()

#remove standard deviation column since it contains blanks
del df['std_pos']
df.head()

################################################################# SCALING THE DATA #######################################################################

# define min max scaler
scaler = MinMaxScaler()

# transform data
X = scaler.fit_transform(df.to_numpy())
X = pd.DataFrame(X)
X.head()

############################################################ ELBOW METHOD FROM YOUTUBE #####################################################################

# Collecting the distortions into list
distortions = []
K = range(1,10)
for k in K:
 kmeanModel = KMeans(n_clusters=k)
 kmeanModel.fit(X)
 distortions.append(kmeanModel.inertia_)
 
# Plotting the distortions
plt.figure(figsize=(16,8))
plt.plot(K, distortions,'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('Elbow Method')
plt.show()

############################################################## K-MEANS FROM YOUTUBE ############################################################################
#Create K-Means Object 
kmeans = KMeans(n_clusters=5)

#fit the data to the model and apply the cluster numbers to the dataframe
X['cluster'] = kmeans.fit_predict(X)

X0 = X[X.cluster==0] 
X1 = X[X.cluster==1]
X2 = X[X.cluster==2]
X3 = X[X.cluster==3]
X4 =X[X.cluster==4]

print(X0)
print(X1)
print(X2)
print(X3)
print(X4)

#Assign the clusters to a variable
centers = kmeans.cluster_centers_

#print clusters
print(centers)

#finding unique clusters
df['cluster'].unique()

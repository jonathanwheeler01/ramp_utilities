# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:15:29 2022

@author: kaypo
"""

#import libraries
import pandas as pd

#import data file
df = pd.read_csv('./data/metadata_clustering_data/subject_clustering/subject_metadata.csv')

#group by id
agg_df= df.groupby('id').agg(lambda x: x.tolist())

#check data type of agg_df
type(agg_df)

#create an id column based on the indexed id column
agg_df['id'] = agg_df.index

#reindex

#check that the new column has been created
agg_df.columns

#create a dataframe that only contains the id and value columns to analyze
metadata_and_id = agg_df[['id','value']]
metadata_and_id.reset_index()

#check the dataframe
metadata_and_id.columns
metadata_and_id.head()

#export aggragated data frame
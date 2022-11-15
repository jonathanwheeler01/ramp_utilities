# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:31:18 2022

@author: kaypo
"""

#%% import libraries
import pandas as pd
import numpy as np
import scipy as sp
import nltk

#%% upload data
data = pd.read_csv('./data/metadata_clustering_data/subject_clustering/aggregated_subject_metadata.csv') 

#%% check data file
data.head()

#%%
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
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


#%% upload data
data = pd.read_csv('./data/metadata_clustering_data/subject_clustering/aggregated_subject_metadata.csv') 

#%% check data file
data.head()
data.info()

#%% apply preprocessing

stop = set(stopwords.words('english'))

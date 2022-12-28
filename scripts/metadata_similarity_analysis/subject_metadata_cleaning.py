# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:31:18 2022

@author: kaypo
"""

#%% import libraries
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import string


#%% upload data
data = pd.read_csv('./data/metadata_clustering_data/subject_clustering/aggregated_subject_metadata.csv') 

#%% check data file
data.head()
data.info()

#%% apply preprocessing

stop = set(stopwords.words('english'))

#punctuation
exclude = set(string.punctuation)

#lemmatization
lemma = WordNetLemmatizer()

#stemming
stemmer = SnowballStemmer('english')

#function for all cleaning steps:
def clean(doc):
    
  # convert text into lower case + split into words
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    
    # remove any punctuation
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)  
   
    # remove digits 
    out_string = ''.join(i for i in punc_free if not i.isdigit())
    
    # normalize the text
    #normalized = " ".join(lemma.lemmatize(word) for word in out_string.split())  
    normalized = " ".join(stemmer.stem(word) for word in out_string.split()) 
    stop_free = " ".join([i for i in normalized.lower().split() if i not in stop])
    
    #remove non-ascii letters
    english_only = "".join(char for char in stop_free if ord(char) < 128)
    
    # remove duplicate words
    remove_duplicates = ' '.join(dict.fromkeys(string.split()))

    return english_only


data['clean_value'] = data['value'].apply(clean)

#%% preview clean data
data.head()
#%% create new data file with clean data only
clean_data = data.copy()
del clean_data['value']

#%% remove records with no metadata
clean_data.dropna(subset=['clean_value'], inplace = True)
clean_data.info()

#%% save clean data file for inspection
clean_data.to_csv('./data/metadata_clustering_data/subject_clustering/clean_subject_metadata.csv')

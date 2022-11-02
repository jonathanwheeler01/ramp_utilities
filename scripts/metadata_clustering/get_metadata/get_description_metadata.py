# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 13:36:15 2022

@author: kaypo
"""

#%%import libraries
import pandas as pd
import sqlite3

#%% query database to collect dspace roots

con = sqlite3.connect("./metadata_database/metadata_database.db")
cur = con.cursor()
res = cur.execute("SELECT oairoot FROM repositories WHERE platform =  'dspace'")
res_list= []
res_list= res.fetchall()

#%%clean dspace roots
#convert from list of tuples to list of strings
draft1_dspace_list = ['/'.join(str(item) for item in res_list)]
draft1_dspace_list = draft1_dspace_list[0].split('/')

#%%remove NONE values and create a new list of strings
draft2_dspace_list = []
for i in draft1_dspace_list:
    if i != '(None,)':
        draft2_dspace_list.append(i)
    else:
        continue
        
#%%remove characters from new string list using translate
final_dspace_list = []
for i in draft2_dspace_list:
    i = i.translate({ord('('): None,
                     ord(')'): None,
                     ord("'"): None,
                     ord("["): None,
                     ord("]"): None,
                     ord(','): None})
    final_dspace_list.append(i)  
   
#%%remove russian repositories content
russ_repos = ['elar.urfu.ru', 'elar.uspu.ru']
for x in russ_repos:
    final_dspace_list.remove(x)
    
#%%create function to grab subject metadata from the database
def get_meta(oairoot):
    con = sqlite3.connect("./metadata_database/metadata_database.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM records WHERE id LIKE '%" + oairoot + "%' AND tag ='description'" )
    res_list = []
    for r in res.fetchall():
        res_list.append(r)
    res_df = pd.DataFrame(res_list, columns=['id', 'namespace', 'tag', 'value'])
    return res_df

#%%iterate over the oairoots stored in newest_list
metadata = pd.DataFrame(columns=['id', 'namespace','tag', 'value'])

for i in final_dspace_list:
   result = get_meta(i)
   metadata = pd.concat([result, metadata], axis=0)
   print(i +' is finished')
   
#%%reindex metadata dataframe
metadata = metadata.reset_index()
metadata.drop('index', axis =1, inplace=True)
metadata.info()

#%%export file
metadata.to_csv('.data/metadata_clustering_data/description_clustering/description_metadata.csv')

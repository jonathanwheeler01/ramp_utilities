# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:32:24 2022

@author: MayeKaypounyers
"""

#import libraries
import pandas as pd
import sqlite3

# query database to collect dspace roots

con = sqlite3.connect("./OneDrive/Desktop/metadata_database.db")
cur = con.cursor()
res = cur.execute("SELECT oairoot FROM repositories WHERE platform =  'dspace'")
res_list= []
res_list= res.fetchall()

#clean dspace roots
#convert from list of tuples to list of strings
string_list = ['/'.join(str(item) for item in res_list)]
string_list = string_list[0].split('/')

#remove NONE values and create a new list of strings
new_string = []
for i in string_list:
    if i != '(None,)':
        new_string.append(i)
    else:
        continue
        
#remove characters from new string list using translate
newest_string = []
for i in new_string:
    i = i.translate({ord('('): None,
                     ord(')'): None,
                     ord("'"): None,
                     ord("["): None,
                     ord("]"): None,
                     ord(','): None})
    newest_string.append(i)  
# create function to grab subject metadata from the database
def get_meta(oairoot):
    con = sqlite3.connect("./OneDrive/Desktop/metadata_database.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM records WHERE id LIKE '%" + oairoot + "%' AND tag ='subject'" )
    res_list = []
    for r in res.fetchall():
        res_list.append(r)
    res_df = pd.DataFrame(res_list, columns=['id', 'namespace', 'tag', 'value'])
    return res_df

#iterate over the oairoots stored in newest_list
metadata = pd.DataFrame(columns=['id', 'namespace','tag', 'value'])

for i in newest_string:
   result = get_meta(i)
   metadata = pd.concat([result, metadata], axis=0)
   print(metadata['id'].unique())
   print(i +' is finished')
   print (metadata.info())
   
   
#reindex metadata dataframe
metadata.reindex()

#combine with clustered data


#export file
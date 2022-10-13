# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:32:24 2022

@author: MayeKaypounyers
"""

#import libraries
import pandas as pd
import sqlite3
import numpy as np
import os

#import metadata
def get_meta(oairoot):
    con = sqlite3.connect('./metadata_database/repository_database.sqbpro')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM records WHERE id LIKE '%" + oairoot + "%'")
    res_list = []
    for r in res.fetchall():
        res_list.append(r)
    res_df = pd.DataFrame(res_list, columns=['id', 'namespace', 'tag', 'value'])
    return res_df

get_meta("https://krex.k-state.edu/dspace")


#format metadata

#export descriptive metadata

#export subject metadata
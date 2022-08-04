import pandas as pd
import sqlite3
import json

# Create a connection to a database
con = sqlite3.connect('../metadata_database/irmeta.sqlite')

# intialize a cursor to interact with the database
cur = con.cursor()

# run a query
res = cur.execute('SELECT count(*) FROM repositories')

# see the result
print(res.fetchone())

# use RAMP_repository_info file as a lookup table
ramp_info = pd.read_csv('../supplementary_data/RAMP_repository_info.csv')

ramp_info.info()

# just dspace IR

dspace_ir = ramp_info[ramp_info['ir_platform'] == 'dspace']

# don't bother with IR that have no metadata
def metadata_check(repository_id):
    with open("../supplementary_data/unified_ids.json") as jd:
        ir_info = json.load(jd)
    for k, v in ir_info.items():
        if repository_id == list(v.keys())[0]:
            ir_ids = list(v.values())[0]
            ir_has_metadata = records_query(ir_ids)
            return ir_has_metadata
            

def records_query(ir_ids):
    records_ct = 0
    con = sqlite3.connect('../metadata_database/irmeta.sqlite')
    cur = con.cursor()
    res = cur.execute('SELECT ir FROM oairoot')
    ir_ids_from_db = res.fetchall()
    ir_id_list = []
    for ir_id in ir_ids_from_db:
        ir_id_list.append(ir_id[0])
    for i in ir_ids:
        if i in ir_id_list:
            oairootq = cur.execute('SELECT oairoot FROM oairoot where ir=:ir_identifier', {'ir_identifier': i})
            oairoot = oairootq.fetchone()[0]
            print(i, oairoot)
        


dspace_ir['repository_id'].apply(metadata_check)


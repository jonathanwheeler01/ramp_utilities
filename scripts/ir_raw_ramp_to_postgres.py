from utilities import *   # pandas is imported here
import glob
import psycopg2
import json


def subset_ramp_by_ir(ir_id, ir_platform):
    # get a list of zip files
    zipfile_list = glob.glob("../zipped_data/*/*page-clicks.zip")

    # insert into postgres one month at a time
    for f in zipfile_list:
        print(f)
        ir_data = extract_subset_ramp_data(f, ir_id)
        ir_data = construct_item_uids(ir_data, ir_platform)
        for i, r in ir_data.iterrows():
            r_id = r['repository_id']
            r_i = r['index']
            r_pos = r['position']
            r_cc = r['citableContent']
            r_ct = r['clickThrough']
            r_url = r['url']
            r_im = r['impressions']
            r_dt = r['date']
            r_c = r['clicks']
            r_uri = r['unique_item_uri']
            cur.execute("INSERT INTO rampraw (repository_id, index, position, citablecontent, clickthrough, url, impressions, date, clicks, unique_item_uri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (r_id, r_i, r_pos, r_cc, r_ct, r_url, r_im, r_dt, r_c, r_uri))
        conn.commit()
        
    print(ir_id, "done!")

    return

# connect to postgres database
with open("../config_files/config.json", "r") as c:
    config = json.load(c)
db = config["dbname"]
u = config["user"]
pwd = config["password"]
conn = psycopg2.connect("dbname='%s' user='%s' password='%s'" % (db, u, pwd))
cur = conn.cursor()

# create a list of zip files
# we only want page-click data
filelist = glob.glob("../raw_zipped_data/*/*_page-clicks.zip")

# read the RAMP_repository_info
ramp_ir_info = pd.read_csv("../supplementary_data/RAMP_repository_info.csv")

# for now we will only insert data for IR included in the study
# (dspace IR)
for i, r in ramp_ir_info.iterrows():
    if r['ir_platform'] == 'dspace':
        repo_id = r['repository_id']
        print("begin insert for", repo_id)
        subset_ramp_by_ir(repo_id, r["ir_platform"])
            
cur.close()
conn.close()
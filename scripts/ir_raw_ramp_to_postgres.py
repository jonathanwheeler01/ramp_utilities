import pandas as pd
import glob
import psycopg2


# create a list of zip files
# we only want page-click data
filelist = glob.glob("../raw_zipped_data/*/*_page-clicks.zip")

# read the RAMP_repository_info
ramp_ir_info = pd.read_csv("../supplementary_data/RAMP_repository_info.csv")

# for now we will only insert data for IR included in the study
# (dspace IR)
for i, r in ramp_ir_info.iterrows():
    if r['ir_platform'] == 'dspace':
        print(r['repository_id'])
        
        
ramp_data = pd.read_csv(filelist[0])
ramp_data.info()

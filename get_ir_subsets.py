import glob
from utilities import *   # pandas is imported here


# Read the IR info file
ir_info = pd.read_csv("RAMP_repository_info.csv")
# print(ir_info.info())

# Create a list of IR to exclude as needed
excluded_ir = ['university_waterloo', 'boston_university']

# get a list of zip files
zipfile_list = glob.glob("./zipped_data/*/*.zip")
# print(zipfile_list)

# To test things we will use an 'included_ir' list
included_ir = ['montana_state_university']

for i, r in ir_info.iterrows():
    if r["ir_platform"] == "dspace":
        if r["repository_id"] in included_ir:
        # if r["repository_id"] not in excluded_ir:
            ir_id = r["repository_id"]
            print("\n", ir_id)
            # Create a dataframe for the IR's RAMP data
            # by reading and subsetting the first zip file
            print(zipfile_list[0])
            ir_data = extract_subset_ramp_data(zipfile_list[0], ir_id)

            # concatenate data from other months
            for f in zipfile_list[1:]:
                print(f)
                mo_data = extract_subset_ramp_data(f, ir_id)
                ir_data = pd.concat([ir_data, mo_data])

            print("\nnrows in dataframe:", len(ir_data))

            ir_data = construct_item_uids(ir_data, "dspace")
            ir_data.to_csv("./ir_data_subsets/" + ir_id + "_RAMP_data.csv", index=False)
            print(ir_id, "done!")



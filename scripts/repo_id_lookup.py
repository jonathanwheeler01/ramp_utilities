import json


with open("../supplementary_data/unified_ids.json", "r") as jd:
    repo_ids = json.load(jd)

index_lookup = input("Enter the index name of the repository: ")

for key, value in repo_ids.items():
    for k, v in value.items():
        if index_lookup in v:
            print(k)




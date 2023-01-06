# serp_and_metadata_clustering_and_similarity_analysis

A directory for clustering and similarity analysis scripts used to analyze 2020 Repository Analytics Metrics Portal (RAMP) data. The scripts (1) cluster resources from DSpace repositories participating in RAMP based on search engine performance metrics provided by the Google Console and (2) determine the subject (DC metadata) similarity of resources that have been clustered together.
```
The information below outlines the scripts included in the directory, including each script's output location
```
**2020 RAMP Data Cleaning and Formatting**
Since multiple links can point to the same resources, the raw RAMP data must be aggregated to ensure that each record in the dataset points to a unique resource instead of a unique link. 
<br>Only repositories supported by DSpace were used in this analysis.	Python, pandas, regular expressions	utilities.py
<br>combines data files – created by project mentor for frequently needed cleaning protocols

agg_and_subset/get_ir_subsets.py
<br>determines which IRs to include in final data subsets to be analyzed
<br>outputs to …/data/ir_data_subsets

agg_and_subset/item_aggregation.py 
<br>used to combine rows by unique_item_uri
<br>outputs to …/data/ir_subsets_itemagg

**RAMP/Search Engine Results Page Performance Data Clustering**
(scripts/ serp_clustering)	
<br>Python, sklearn, pandas, numpy, K-Means Clustering	

<br>serp_clustering/create_serp_clusters.py
<br>creates resource clusters based on search engine performance data collected from the Google Console Services. The code allows for a user to determine which <br>search engine performance features to include in the clustering protocol
<br>outputs to …/data/serp_clustering_data/serp_clusterd_data

serp_clustering/inspect_serp_clusters
<br>determines descriptive metrics for each cluster – mean values, IQR, etc.
<br>outputs to …/data/serp_clustering_data/serp_cluster_summaries

**Extract Subject Metadata**
(scripts/get_metadata)
<br>Python, SQLite, OAI-PHM (not included in the stored code – request made by project mentor), pandas	get_metadata/get_subject_metadata.py 
<br>extracts subject metadata for each resource included in the previous search engine performance clustering analysis
<br>outputs to …/data/metadata_similarity_data/subject_metadata

**Determine Subject Similarity of Clustered Resources**
(scripts/metadata_similarity_analysis)
<br>Only English and Spanish language metadata was used for clustering.	Python, pandas, nltk, matplotlib, numpy, sklearn <br>metadata_similarity_analysis/aggregate_sub_metadata_by_item.py 
<br>aggregates subject metadata by unique resource from RAMP IRs
<br>outputs to …/data/metadata_similarity_data/aggregated_subject_metadata

metadata_similarity_analysis/subject_metadata_cleaning.py 
<br>cleans metadata by removing non-English and non-Spanish language metadata among other tasks – tokenization, special character cleaning, etc. 
<br>outputs to …/data/metadata_similarity_data/clean_subject_metadata

determine_cluster_similarity_cosine_1gram.py 
<br>determines the subject term similarity of resources with similar search engine performance metrics
<br>outputs to …/data/metadata_similarity_data/cluster3_metadata…
<br>outputs to …/data/metadata_similarity_data/similarity_matrix…



With the exception of the *RAMP_repository_info.csv* file, all files except R and Python scripts should be excluded from the repository. Please update the ```.gitignore``` file as needed.

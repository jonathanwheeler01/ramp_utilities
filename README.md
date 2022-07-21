# RAMP utilities

A repository for functions and methods that are helpful in analyzing RAMP data. The main file of interest is ```utilities.py```, which can be imported into scripts:

```
from utilities import *
```

Scripts demonstrating common workflows are also included.

The repository includes two empty directories, *zipped_data* and *ir_data_subsets*. Raw data in zipped format downloaded from Dryad can be added to the *zipped_data* directory. Git will ignore these files.

It is often useful to subset RAMP data by IR prior to analysis. The script ```get_ir_subsets.py``` does this, and saves a CSV file of output data for each IR in the *ir_data_subsets* directory. Git will also ignore these files.

With the exception of the *RAMP_repository_info.csv* file, all files except R and Python scripts should be excluded from the repository. Please update the ```.gitignore``` file as needed.

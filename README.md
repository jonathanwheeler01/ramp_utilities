# RAMP utilities

A repository for functions and methods that are helpful in analyzing RAMP data. 

With the exception of the *RAMP_repository_info.csv* file, all files except R 
and Python scripts should be excluded from the repository. 
Please update the ```.gitignore``` file as needed.

## Utilities

The main file of interest is ```utilities.py```, which can be imported into 
scripts:

```
from utilities import *
```

## Workflows

All workflows described below require raw RAMP data in zipped format,
available in yearly datasets from the Dryad data repository. Although data are
available going back to 2017, it is recommended to use data from 2019
onward:

> 2019: <https://doi.org/10.5061/dryad.crjdfn342>
> 2020: <https://doi.org/10.5061/dryad.dv41ns1z4>
> 2021: <https://doi.org/10.5061/dryad.1rn8pk0tz>

As required, paths to downloaded data should be updated.

### Using local CSV files

1. Raw RAMP data are provided one file per month. It is useful for the purposes
of many analyses to create sets of data per IR, rather than per month. It is
also useful to add an identifier that is unique to items within each IR. Both
of these processes can be accomplished using the file ```get_ir_subsets.py```, 
which requires raw RAMP data in zipped format as input.

2. The per-IR RAMP data output by ```get_ir_subsets.py``` contains search 
engine performace data about specific URLs. An *item* hosted by an IR may
correspond to multiple URLs. In order to analyze IR content at the item level,
it is necessary to aggregate data. The file ```item_aggregation_apply.py``` does
this. The per-IR RAMP data files output from step 1 above are the required
input for this step.

        
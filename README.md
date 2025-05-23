# CMML_mp2
## Data
The original data can be downloaded from [here](https://drive.google.com/drive/folders/1pHmE9cg_tMcouV1LFJFtbyBJNp7oQo9J), located in the `SimulatedDataUpload/dataset1` directory.

## Pipeline
All pipeline code is located in the `code/` directory.

To run Tangram:
```
python Tangram_pipeline.py \
    <single-cell reference h5> \
    <spatial h5> \
    <the obs name of celltype> \
    <output_path>
```

To run Cell2location:
```
python Cell2location_pipeline.py \
    <single-cell reference h5> \
    <spatial h5> \
    <the obs name of celltype> \
    <output_path>
```

To run CARD:
- First, use the `format_card_data.ipynb` notebook to generate data for CARD from your single-cell reference h5 and spatial h5 files.
- Then, run `card_pipeline.R`.

## Environment
Details of package versions can be found in `env_info_python.txt` and `env_info_R.txt`.

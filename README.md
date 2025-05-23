# CMML_mp2
## Data

The original dataset is available [here](https://drive.google.com/drive/folders/1pHmE9cg_tMcouV1LFJFtbyBJNp7oQo9J) in the `SimulatedDataUpload/dataset1` directory.

## Pipeline

All pipeline scripts are located in the `code/` directory.

**To run Tangram:**
```
python Tangram_pipeline.py \
    <single-cell reference h5> \
    <spatial h5> \
    <celltype obs name> \
    <output_path>
```

**To run Cell2location:**
```
python Cell2location_pipeline.py \
    <single-cell reference h5> \
    <spatial h5> \
    <celltype obs name> \
    <output_path>
```

**To run CARD:**
1. Use the `format_card_data.ipynb` notebook to prepare CARD input data from your single-cell and spatial h5 files.
2. Execute `card_pipeline.R` to run the analysis.

## Environment

Package versions and environment details are provided in `env_info_python.txt` and `env_info_R.txt`.

## Results

All output files are saved in the `results/` directory.

## Figures

Figures and the code used to generate them are available in the `code/` directory.
# CMML_mp2

## data
Original data can be downloaded from here https://drive.google.com/drive/folders/1pHmE9cg_tMcouV1LFJFtbyBJNp7oQo9J
in the SimulatedDataUpload/dataset1

## pipeline
All pipeline code are in `code/` directory. 


To run Tangram:
```
python Tangram_pipeline.py \
    <single-cell reference h5>
    <spatial h5> \
    <the obs name of celltype> \
    <output_path>
```

To run Cell2location:
```
python Cell2location_pipeline.py \
    <single-cell reference h5>
    <spatial h5> \
    <the obs name of celltype> \
    <output_path>
```

To run CARD:
- first use the `format_card_data.ipynb` notebook to generate data for CARD from your single-cell reference h5 and spatial h5.
- Run the `card_pipeline.R`

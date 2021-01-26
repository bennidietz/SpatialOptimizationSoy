# SpatialOptimizationSoy

Make sure you download the figures, landuse maps and objectives from the learnweb and paste them into the provided folders as they are obviously gitignored.

Execute the following command in anaconda prompt before running the optimization scripts:

`conda activate opti`

## What data do we need

For both study areas (amazon and cerado) we need:
 - Landuse maps (with at least the classes soy and not soy)
 - temperature data
 - precipitation

## Useful data from learnweb
```
infrastracture.zip
protected_areas.zip
```

# Base data
`mt_2017_v3_1_reprojection.tif` --> used as base landuse map
`soy_new.asc`

## When executed `read_data.py`
1. Reclassified map is saved in `reclass.tiff`

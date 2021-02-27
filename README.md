# Soy cultivation - Spatial Optimization

Spatial Optimization study project at the [ifgi](https://www.uni-muenster.de/Geoinformatics/) at the university of Münster, Germany
\
The goal of this project is to optimize land use pattern in certain investigation areas in two region of Brazil (Cerrado and Amazon). It focusses on the spatial configuration of soy cultivation and its impact on the total soy yield and its water footprint of the region.

### Reproduce this project

As the initial used data are pretty large and are belonging to certain scientific papers (thus where not generated by us), we decided to gitignore them. Thus they need to be downloaded an included beforehand. You can find the data here:

- [a - Ready classified land use maps for Mato Grosso from 2001 to 2017](https://www.nature.com/articles/s41597-020-0371-4)
- [b - Qualified potential soy yield values for Mato Grosso](https://webarchive.iiasa.ac.at/Research/LUC/GAEZv3.0/)
- [c - Temperatur and precipitation data for whole Brazil](http://careyking.com/data-downloads/)

Following files are necessary in the `/data/base`-directory:
- 'mt_2017_v3_1_reprojection.tif' - base classified image for Cerrado (from **source a**)
- 'soy_new.asc' - potential soy yield (from **source b**)
- precipitation and temperature data for cropped and interpolated on our own which can be reproduced through our R scripts

### Scripts (found in `/scripts`-directory) and their job
- **read_data.py**: preprocesses the data
- **run_optimization.py**: defines the problem and the correspondent algorithm and exectutes the optimization

### Results
Some of the results running the algorithm with 500 generations, 10 offsprings and an initial population of 100 can be seen in the `results`-directory.

#### Optimized land use
<center> <h5>Investigation area in Cerrado</h5> </center>
<img src="https://github.com/bennidietz/SpatialOptimizationSoy/blob/main/results/landuse_max_Cerrado.png?raw=true">
<center> <h5>Investigation area in Amazon</h5> </center>
<img src="https://github.com/bennidietz/SpatialOptimizationSoy/blob/main/results/landuse_max_amazon.png?raw=true">

### Objective space (pareto front)
<center> <h5>Investigation area in Cerrado</h5> </center>
<img src="https://github.com/bennidietz/SpatialOptimizationSoy/blob/main/results/objective_space_Cerrado.png?raw=true">
<center> <h5>Investigation area in Amazon</h5> </center>
<img src="https://github.com/bennidietz/SpatialOptimizationSoy/blob/main/results/objective_space_amazon.png?raw=true">

### Change of objectives over generations
<center> <h5>Investigation area in Cerrado</h5> </center>
<img src="https://github.com/bennidietz/SpatialOptimizationSoy/blob/main/results/objectives_over_generations_Cerrado.png?raw=true">
<center> <h5>Investigation area in Amazon</h5> </center>
<img src="https://github.com/bennidietz/SpatialOptimizationSoy/blob/main/results/objectives_over_generations_amazon.png?raw=true">


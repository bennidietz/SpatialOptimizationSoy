install.packages("devtools")
library(devtools)
if (!require("rspatial")) devtools::install_github('rspatial/rspatial')
library(rspatial)

dsp <- SpatialPoints(points, proj4string=CRS("+proj=longlat +datum=WGS84"))
dsp <- SpatialPointsDataFrame(dsp, d)
CA <- sp_data("counties")
# define groups for mapping
cuts <- c(0,200,300,500,1000,3000)
# set up a palette of interpolated colors
blues <- colorRampPalette(c('yellow', 'orange', 'blue', 'dark blue'))
pols <- list("sp.polygons", CA, fill = "lightgray")
spplot(dsp, 'prec', cuts=cuts, col.regions=blues(5), sp.layout=pols, pch=20, cex=2)

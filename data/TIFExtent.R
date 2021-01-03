# install packages if not yet done
install.packages(raster)
install.packages(rstudioapi)
install.packages("R.matlab")
install.packages("mapboxer")
install.packages("netcdf4")

# import packages and set base working directory
library(raster)
library(rstudioapi)
library(netcdf4)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

landuse_map = raster("mt_2017_v3_1_reprojection.tif")
temperatur_map = readMat("tmin_tmax_Avery.mat")

mean_Tmax = colMeans(temperatur_map$tmax,na.rm=TRUE)
mean_Tmin = colMeans(temperatur_map$tmin,na.rm=TRUE)
meanAverage = (mean_Tmax + mean_Tmin) / 2

new_matrix = matrix(c(temperatur_map$ID.lat.lon.alt, meanAverage),803)

startPoint = c(extent(landuse_map)[1],
              extent(landuse_map)[4])
endPoint = c(extent(landuse_map)[2],
               extent(landuse_map)[3])

# amazon: y: 900:1500, x: 600:1600
# cerrado: 3700:4300,4000:5000
getAbsoulteCoordinates <- function(x, y) {
  point = c(startPoint[1] + res(landuse_map)[1] * x,
            startPoint[2] - res(landuse_map)[2] * y)
  return (point)
}

amazon_topLeft = getAbsoulteCoordinates(600, 900)
amazon_bottomRight = getAbsoulteCoordinates(1600, 1500)
bbox_amazon = c(amazon_topLeft, amazon_bottomRight)

cerrado_topLeft = getAbsoulteCoordinates(4000, 3700)
cerrado_bottomRight = getAbsoulteCoordinates(5000, 4300)
bbox_cerrado = c(cerrado_topLeft, cerrado_bottomRight)

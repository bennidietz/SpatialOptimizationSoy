setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
install.packages("leaflet")
library(sp)
library(leaflet)
library(R.matlab)

bbox_amazon = c(-60.530319,  -8.954522, -58.636405, -10.090870)
bbox_cerrado = c(-54.09101, -14.25748, -52.19710, -15.39383)

weather2 = readMat("weather2.mat")
temperatur_map = readMat("tmin_tmax_Avery.mat")

mean_Tmax = colMeans(temperatur_map$tmax,na.rm=TRUE)
mean_Tmin = colMeans(temperatur_map$tmin,na.rm=TRUE)
meanAverage = (mean_Tmax + mean_Tmin) / 2

new_matrix = matrix(c(temperatur_map$ID.lat.lon.alt, meanAverage),803)

getAllPointsWithinBbox = function(allPoints, bbox) {
  points = c()
  for (i in 1:length(allPoints[,1])) {
    lat = allPoints[i,][2]
    lon = allPoints[i,][3]
    if (lat <= bbox[2] && lat >= bbox[4] && lon >= bbox[1] && lon <= bbox[3]) {
      p = c(allPoints[i,][3], allPoints[i,][2], allPoints[i,][5])
      points = append(points, p)
    }
  }
  return(matrix(points,3,byrow=TRUE))
}

points = getAllPointsWithinBbox(new_matrix, bbox_cerrado)
print(points)

coors = new_matrix[,2:3]
leaflet() %>% addTiles() %>%
  addMarkers(coors[,2], coors[,1], popup = "~htmlEscape(Name)")

#coordinates(df) <- ~longitude+latitude
#leaflet(df) %>% addMarkers() %>% addTiles()

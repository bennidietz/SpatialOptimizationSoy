#https://unidata.github.io/netcdf4-python/netCDF4/index.html
#https://stackoverflow.com/questions/29135885/netcdf4-extract-for-subset-of-lat-lon
#https://utexas.app.box.com/v/Xavier-etal-IJOC-DATA/folder/40983701074

import settings
from netCDF4 import Dataset
import numpy as np

#function that calculates mean values from multidimensional arrays of netcdf files

def calculateNCMeanValues(dataArray):
    meanValues = []
    meanData = sum(dataArray[:]) / len(dataArray[:])

    return meanData

#open datasets

data_prec = Dataset(settings.get_file_prec(), mode='r')
data_tmin = Dataset(settings.get_file_tmin(), mode='r')
data_tmax = Dataset(settings.get_file_tmax(), mode='r')

#crop dataset => subset creation
#latitude lower and upper index / longitude lower and upper index

#precipitation (mm)

lats = data_prec.variables['latitude'][:]
lons = data_prec.variables['longitude'][:]

latli = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[1]))

prec_amazon = data_prec.variables['prec'][:, latli:latui, lonli:lonui]
prec_amazon = calculateNCMeanValues(prec_amazon)
#print(prec_amazon)

latli = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[1]))

prec_cerrado = data_prec.variables['prec'][:, latli:latui, lonli:lonui]
prec_cerrado = calculateNCMeanValues(prec_cerrado)
#print(prec_cerrado)

print("Precipitation data loaded and cropped. The average values for the " + str(len(data_prec.variables['prec'])) + " timesteps have been calculated.")

#tmin (Celsius)

lats = data_tmin.variables['latitude'][:]
lons = data_tmin.variables['longitude'][:]

latli = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[1]))

tmin_amazon = data_tmin.variables['Tmin'][:, latli:latui, lonli:lonui]
tmin_amazon = calculateNCMeanValues(tmin_amazon)
#print(tmin_amazon)

latli = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[1]))

tmin_cerrado = data_tmin.variables['Tmin'][:, latli:latui, lonli:lonui]
tmin_cerrado = calculateNCMeanValues(tmin_cerrado)
#print(tmin_cerrado)

print("Tmin data loaded and cropped. The average values for the " + str(len(data_tmin.variables['Tmin'])) + " timesteps have been calculated.")

#tmax (Celsius)

lats = data_tmax.variables['latitude'][:]
lons = data_tmax.variables['longitude'][:]

latli = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[1]))

tmax_amazon = data_tmax.variables['Tmax'][:, latli:latui, lonli:lonui]
tmax_amazon = calculateNCMeanValues(tmax_amazon)
#print(tmax_amazon)

latli = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[1]))

tmax_cerrado = data_tmax.variables['Tmax'][:, latli:latui, lonli:lonui]
tmax_cerrado = calculateNCMeanValues(tmax_cerrado)
#print(tmax_cerrado)

print("Tmax data loaded and cropped. The average values for the " + str(len(data_tmax.variables['Tmax'])) + " timesteps have been calculated.")

#calculate average/median values for temperature from tmin and tmax for both areas

temp_amazon = (np.array(tmin_amazon) + np.array(tmax_amazon)) / 2.0
temp_cerrado = (np.array(tmin_cerrado) + np.array(tmax_cerrado)) / 2.0

print("Temperature data for amazon and cerrado have been calculated.")

#store data files in data folder

np.save(settings.get_file_prec_amazon(), np.array(prec_amazon))
np.save(settings.get_file_prec_cerrado(), np.array(prec_cerrado))
np.save(settings.get_file_temp_amazon(), np.array(temp_amazon))
np.save(settings.get_file_temp_cerrado(), np.array(temp_cerrado))

print("Stored precipitation and temperature files in data directory.")

#"interpolate" data to a full size grid

n_cells = 400
prec_amazon_scaled = np.kron(prec_amazon, np.ones((n_cells, n_cells)))

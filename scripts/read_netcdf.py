#https://unidata.github.io/netcdf4-python/netCDF4/index.html
#https://stackoverflow.com/questions/29135885/netcdf4-extract-for-subset-of-lat-lon
#https://utexas.app.box.com/v/Xavier-etal-IJOC-DATA/folder/40983701074

import settings
from netCDF4 import Dataset
import numpy as np

#open datasets

data_prec = Dataset(settings.get_file_prec(), mode='r')
data_tmin = Dataset(settings.get_file_tmin(), mode='r')
data_tmax = Dataset(settings.get_file_tmax(), mode='r')

#crop dataset => subset creation
#latitude lower and upper index / longitude lower and upper index

#precipitation

lats = data_prec.variables['latitude'][:]
lons = data_prec.variables['longitude'][:]

latli = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_amazon_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_amazon_lon_bounds()[1]))

prec_amazon = data_prec.variables['prec'][:, latli:latui, lonli:lonui]
print(prec_amazon)

latli = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[0]))
latui = np.argmin(np.abs(lats - settings.get_bounding_box_cerrado_lat_bounds()[1]))
lonli = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[0]))
lonui = np.argmin(np.abs(lons - settings.get_bounding_box_cerrado_lon_bounds()[1]))

prec_cerrado = data_prec.variables['prec'][:, latli:latui, lonli:lonui]
print(prec_cerrado)

#tmin

#to do

#tmax

#to do

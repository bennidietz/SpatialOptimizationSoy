#https://unidata.github.io/netcdf4-python/netCDF4/index.html
#https://stackoverflow.com/questions/29135885/netcdf4-extract-for-subset-of-lat-lon
#https://utexas.app.box.com/v/Xavier-etal-IJOC-DATA/folder/40983701074

from netCDF4 import Dataset
import numpy as np
import os

default_directory = os.path.dirname(os.path.realpath(__file__))

filename = "prec_monthly_UT_Brazil_v2_198001_201312.nc"
file = default_directory + "/" + filename

data = Dataset(file, mode='r')
#print(data)
#print(data.variables)

#crop dataset => precipitation subset

print(data.variables['latitude'][:])
print(data.variables['longitude'][:])
#print(data.variables['prec'][:])
#print(dir(data.variables['latitude']))
#print(data.variables['latitude'].dimensions())

#limitsLat = [-35, 7]
#limitsLon = [-75, -31]

#first bounding box: -8.954522, -60.530319 -> -10.090870, -58.636405
#second bounding box: -14.25748, -54.09101 -> -15.39383, -52.19710

latbounds = [-10.090970, -8.954522]
lonbounds = [-60.530319, -58.636405]

#latbounds = [-15.39383, -14.25748]
#lonbounds = [-54.09101, -52.19710]

lats = data.variables['latitude'][:]
lons = data.variables['longitude'][:]

# latitude lower and upper index
latli = np.argmin(np.abs(lats - latbounds[0]))
latui = np.argmin(np.abs(lats - latbounds[1]))

# longitude lower and upper index
lonli = np.argmin(np.abs(lons - lonbounds[0]))
lonui = np.argmin(np.abs(lons - lonbounds[1]))

precSubset = data.variables['prec'][:,latli:latui, lonli:lonui]
print(precSubset)

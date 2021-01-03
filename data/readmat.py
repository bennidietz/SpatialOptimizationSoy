#required to read mat files from version 7.3

import h5py
import numpy as np
import scipy.io
import os

default_directory = os.path.dirname(os.path.realpath(__file__))
filename = "weather2.mat"

filepath = default_directory + "/" + filename
arrays = {}
f = h5py.File(filepath)
for k, v in f.items():
    arrays[k] = np.array(v)

print(arrays)
#print(type(arrays.get('weather2')))
#print(arrays.get('weather2').get('coordinates'))
#print(dir(arrays.get('weather2')))

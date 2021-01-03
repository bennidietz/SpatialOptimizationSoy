from netCDF4 import Dataset
import numpy as np
import os

default_directory = os.path.dirname(os.path.realpath(__file__))

filename_prec_data = default_directory + "/prec_daily_UT_Brazil_v2.1_20100101_20151231.nc"
filename_ex_file = default_directory + "/sresa1b_ncar_ccsm3-example.nc"

ds = Dataset(filename_prec_data, mode='r')
print(ds)
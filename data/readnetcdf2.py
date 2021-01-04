#execute before: conda install --channel conda-forge cartopy
#https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing

import nctoolkit as nc
import os
from multiprocessing import Process

default_directory = os.path.dirname(os.path.realpath(__file__))
filename = "prec_monthly_UT_Brazil_v2_198001_201312.nc"
file = default_directory + "/" + filename

nc.options(lazy=True)
data = nc.open_data(file)
data.crop(lon = [-60.530319, -15.39383], lat = [-52.19710, -8.954522])

if __name__ == '__main__':

    data.to_nc("clip.nc")

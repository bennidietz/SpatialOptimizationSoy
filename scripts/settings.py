import os, sys

#base settings

default_directory = os.path.dirname(os.path.realpath(__file__))
data_directory = default_directory + '/../data'

#files

file_landuse = "mt_2017_v3_1_reprojection.tif"
file_landuse_colored = "MatoGrosso_2017_original.tif"
file_landuse_reclass = "MatoGrosso_2017_reclass.tif"

file_reclass_amazon_tif = "reclass_amazon.tif"
file_reclass_amazon_npy = "landuse_amazon.npy"
file_reclass_cerrado_tif = "reclass_cerrado.tif"
file_reclass_cerrado_npy = "landuse_cerrado.npy"

file_soy = "soy_new.asc"
file_soy_amazon = "soy_potential_yield_amazon.pkl"
file_soy_cerrado = "soy_potential_yield_cerrado.pkl"

#use either daily OR monthly data for ALL of these!

file_prec = "prec_daily_UT_Brazil_v2.2_20100101_20151231.nc"
file_tmin = "Tmin_daily_UT_Brazil_v2_20140101_20170731_s1.nc"
file_tmax = "Tmax_daily_UT_Brazil_v2_20140101_20170731_s1.nc"

file_prec_amazon = "prec_amazon.npy"
file_prec_cerrado = "prec_cerrado.npy"
file_temp_amazon = "temp_amazon.npy"
file_temp_cerrado = "temp_cerrado.npy"

file_prec_amazon_interpolated = "prec_amazon_interpolated.npy"
file_prec_cerrado_interpolated = "prec_cerrado_interpolated.npy"
file_temp_amazon_interpolated = "temp_amazon_interpolated.npy"
file_temp_cerrado_interpolated = "temp_cerrado_interpolated.npy"

#bounding boxes

bounding_box_amazon_lat_bounds = [-10.46965, -9.712087]
bounding_box_amazon_lon_bounds = [-56.458405, -55.70084]

bounding_box_cerrado_lat_bounds = [-15.01504, -14.25748]
bounding_box_cerrado_lon_bounds = [-54.09101, -53.33345]

#output visualizations

#500gen results
directory_500gen = default_directory + '/../Results500gen'
amazon_landuse_result_500gen = "landuse_amazon_500gen.npy"
cerrado_landuse_result_500gen = "landuse_cerrado_500gen.npy"
amazon_objectives_result_500gen = "objectives_amazon_500gen.npy"
cerrado_objectives_result_500gen = "objectives_cerrado_500gen.npy"

#return functions

def get_default_directory(): return default_directory
def get_data_directory(): return data_directory
def get_file_landuse(): return data_directory + "/base/" + file_landuse
def get_file_landuse_colored(): return data_directory + "/base/" + file_landuse_colored
def get_file_landuse_reclass(): return data_directory + "/base/" + file_landuse_reclass
def get_file_reclass_amazon_tif(): return data_directory + "/" + file_reclass_amazon_tif
def get_file_reclass_amazon_npy(): return data_directory + "/" + file_reclass_amazon_npy
def get_file_reclass_cerrado_tif(): return data_directory + "/" + file_reclass_cerrado_tif
def get_file_reclass_cerrado_npy(): return data_directory + "/" + file_reclass_cerrado_npy
def get_file_soy(): return data_directory + "/" + file_soy
def get_file_soy_amazon(): return data_directory + "/" + file_soy_amazon
def get_file_soy_cerrado(): return data_directory + "/" + file_soy_cerrado
def get_file_prec(): return data_directory + "/base/" + file_prec
def get_file_tmin(): return data_directory + "/base/" + file_tmin
def get_file_tmax(): return data_directory + "/base/" + file_tmax
def get_file_prec_amazon(): return data_directory + "/" + file_prec_amazon
def get_file_prec_cerrado(): return data_directory + "/" + file_prec_cerrado
def get_file_temp_amazon(): return data_directory + "/" + file_temp_amazon
def get_file_temp_cerrado(): return data_directory + "/" + file_temp_cerrado
def get_file_prec_amazon_interpolated(): return data_directory + "/" + file_prec_amazon_interpolated
def get_file_prec_cerrado_interpolated(): return data_directory + "/" + file_prec_cerrado_interpolated
def get_file_temp_amazon_interpolated(): return data_directory + "/" + file_temp_amazon_interpolated
def get_file_temp_cerrado_interpolated(): return data_directory + "/" + file_temp_cerrado_interpolated
def get_bounding_box_amazon_lat_bounds(): return bounding_box_amazon_lat_bounds
def get_bounding_box_amazon_lon_bounds(): return bounding_box_amazon_lon_bounds
def get_bounding_box_cerrado_lat_bounds(): return bounding_box_amazon_lat_bounds
def get_bounding_box_cerrado_lon_bounds(): return bounding_box_cerrado_lon_bounds
def get_file_amazon_landuse_results_500gen(): return directory_500gen + "/" + amazon_landuse_result_500gen
def get_file_cerrado_landuse_results_500gen(): return directory_500gen + "/" + cerrado_landuse_result_500gen
def get_file_amazon_objectives_results_500gen(): return directory_500gen + "/" + amazon_objectives_result_500gen
def get_file_cerrado_objectives_results_500gen(): return directory_500gen + "/" + cerrado_objectives_result_500gen

#other default functions

def getEnding(string):
    return "'" + string[string.rindex("/")+1:] + "'"

def printFileCreated(filename):
    print("New file was created at: " + getEnding(filename) + "...")

def printFileAlreadyExists(filename):
    print("The file " + getEnding(filename) + " already exists.")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
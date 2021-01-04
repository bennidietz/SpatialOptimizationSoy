import os

#base settings

default_directory = os.path.dirname(os.path.realpath(__file__))
data_directory = default_directory + '/../data'

#files

file_landuse = "mt_2017_v3_1_reprojection.tif"
file_landuse_colored = "MatoGrosso_2017_original.tif"
file_landuse_reclass = "MatoGrosso_2017_reclass.tif"

file_reclass_amazon_tif = "Reclassified_Crop_Amazon.tif"
file_reclass_amazon_npy = "landuse_map_in_amazon.npy"
file_reclass_cerrado_tif = "Reclassified_Crop_Cerrado.tif"
file_reclass_cerrado_npy = "landuse_map_in_cerrado.npy"

file_soy = "soy_new.asc"
file_soy_amazon = "soy_potential_yield_amazon.pkl"
file_soy_cerrado = "soy_potential_yield_cerrado.pkl"

file_prec = "prec_monthly_UT_Brazil_v2_198001_201312.nc"
file_tmin = "Tmin_daily_UT_Brazil_v2_20140101_20170731_Control_s1.nc"
file_tmax = "Tmax_daily_UT_Brazil_v2_20140101_20170731_Control_s1.nc"

#bounding boxes

bounding_box_amazon_lat_bounds = [-10.090970, -8.954522]
bounding_box_amazon_lon_bounds = [-60.530319, -58.636405]
bounding_box_cerrado_lat_bounds = [-15.39383, -14.25748]
bounding_box_cerrado_lon_bounds = [-54.09101, -52.19710]

#return functions

def get_default_directory(): return default_directory
def get_data_directory(): return data_directory
def get_file_landuse(): return data_directory + "/" + file_landuse
def get_file_landuse_colored(): return data_directory + "/" + file_landuse_colored
def get_file_landuse_reclass(): return data_directory + "/" + file_landuse_reclass
def get_file_reclass_amazon_tif(): return data_directory + "/" + file_reclass_amazon_tif
def get_file_reclass_amazon_npy(): return data_directory + "/" + file_reclass_amazon_npy
def get_file_reclass_cerrado_tif(): return data_directory + "/" + file_reclass_cerrado_tif
def get_file_reclass_cerrado_npy(): return data_directory + "/" + file_reclass_cerrado_npy
def get_file_soy(): return data_directory + "/" + file_soy
def get_file_soy_amazon(): return data_directory + "/" + file_soy_amazon
def get_file_soy_cerrado(): return data_directory + "/" + file_soy_cerrado
def get_file_prec(): return data_directory + "/" + file_prec
def get_file_tmin(): return data_directory + "/" + file_tmin
def get_file_tmax(): return data_directory + "/" + file_tmax
def get_bounding_box_amazon_lat_bounds(): return bounding_box_amazon_lat_bounds
def get_bounding_box_amazon_lon_bounds(): return bounding_box_amazon_lon_bounds
def get_bounding_box_cerrado_lat_bounds(): return bounding_box_amazon_lat_bounds
def get_bounding_box_cerrado_lon_bounds(): return bounding_box_cerrado_lon_bounds

def getEnding(string):
    return "'" + string[string.rindex("/")+1:] + "'"

def printFileCreated(filename):
    print("New file was created at: " + getEnding(filename) + "...")

def printFileAlreadyExists(filename):
    print("The file " + getEnding(filename) + " already exists.")

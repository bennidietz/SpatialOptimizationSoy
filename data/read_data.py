import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import ListedColormap
import pickle
import matplotlib.patches as mpatches
import os

default_directory = os.path.dirname(os.path.realpath(__file__))

# read data from tiff file as numpy array
landuse_original = plt.imread(default_directory + "/mt_2017_v3_1_reprojection.tif")

# plot original landuse map
f1, ax1 = plt.subplots(1)
cmap1 = ListedColormap(["#b3cc33","#be94e8","#1b5ee4", "#10773e", "#000000"])
legend_landuse1 = [
        mpatches.Patch(color="#b3cc33",label = 'Soy'),
        mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
        mpatches.Patch(color="#1b5ee4",label = 'Water'),
        mpatches.Patch(color="#10773e",label = 'Not soy'),
        mpatches.Patch(color="#000000",label = 'No data')
]

# create empty map
rows = landuse_original.shape[0]
cols = landuse_original.shape[1]
landuse_reclass = np.zeros((rows,cols),dtype= 'uint8')
# reclassify landuse map
landuse_reclass[landuse_original == 1] = 4
landuse_reclass[landuse_original == 2] = 4
landuse_reclass[landuse_original == 3] = 4
landuse_reclass[landuse_original == 4] = 4
landuse_reclass[landuse_original == 5] = 1
landuse_reclass[landuse_original == 6] = 1
landuse_reclass[landuse_original == 7] = 1
landuse_reclass[landuse_original == 8] = 1
landuse_reclass[landuse_original == 9] = 1
landuse_reclass[landuse_original == 10] = 4
landuse_reclass[landuse_original == 11] = 2
landuse_reclass[landuse_original == 12] = 3
landuse_reclass[landuse_original == 13] = 4
landuse_reclass[landuse_original == 15] = 5

f2, ax2 = plt.subplots(1)
cmap2 = ListedColormap(["#b3cc33","#be94e8","#1b5ee4", "#10773e", "#000000"])
legend_landuse2 = [
    mpatches.Patch(color="#b3cc33",label = 'Soy'),
        mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
        mpatches.Patch(color="#1b5ee4",label = 'Water'),
        mpatches.Patch(color="#10773e",label = 'Not soy'),
        mpatches.Patch(color="#000000",label = 'No data')
]

im1 = plt.imshow(landuse_reclass,interpolation='none',
    cmap=cmap2, vmin = 0.5, vmax = 10.5)
plt.imsave(default_directory + "/reclass.tiff", landuse_reclass, format = "tiff", cmap = cmap2)

""" 
ax1.set_title('Landuse map original')
ax1.set_xlabel('Column #')
ax1.set_ylabel('Row #')
ax1.legend(handles=legend_landuse2,bbox_to_anchor=(1.05,1), loc=2,
    borderaxespad=0.)
plt.imsave(default_directory +
    "/Landuse_maps/MatoGrosso_2017_original.tif",
    landuse_reclass,format='tiff',cmap=cmap2)
#plt.show()

landuse_clipped = landuse_reclass[2800:2900,1700:1800]
np.save(default_directory + "/Landuse_maps/landuse_map_in.npy",landuse_clipped)
# read potential yield maps from asc file
sugarcane_pot_yield = np.loadtxt(default_directory +
    "/Objectives/sugarcane_new.asc", 
    skiprows=6)[2800:2900,1700:1800]
soy_pot_yield = np.loadtxt(default_directory + 
    "/Objectives/soy_new.asc", 
    skiprows=6)[2800:2900,1700:1800]
cotton_pot_yield = np.loadtxt(default_directory + 
    "/Objectives/cotton_new.asc",
    skiprows=6)[2800:2900,1700:1800]
pasture_pot_yield = np.loadtxt(default_directory + 
    "/Objectives/grass_new.asc", 
    skiprows=6)[2800:2900,1700:1800]

# save the cropped potential yield maps
with open(default_directory + "/Objectives/sugarcane_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(sugarcane_pot_yield, output, pickle.HIGHEST_PROTOCOL)
with open(default_directory + "/Objectives/soy_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(soy_pot_yield, output, pickle.HIGHEST_PROTOCOL)
with open(default_directory + "/Objectives/cotton_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(cotton_pot_yield, output, pickle.HIGHEST_PROTOCOL)
with open(default_directory + "/Objectives/pasture_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(pasture_pot_yield, output, pickle.HIGHEST_PROTOCOL)

plt.imshow(default_directory + "/Objectives/soy_potential_yield_example.pkl",interpolation='none',
    cmap=cmap2, vmin = 0.5, vmax = 10.5) """
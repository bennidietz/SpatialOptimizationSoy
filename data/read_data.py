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
cmap1 = ListedColormap(["#b3cc33","#be94e8","#10773e","#eeefce","#e4a540","#a4507d","#c948a2","#be5b1d", "#f09cde","#877712","#614040","#1b5ee4", "#0cf8c1","#00000000","#00000000"])
legend_landuse1 = [
        mpatches.Patch(color="#be94e8", label = 'Fallow/cotton'),
        mpatches.Patch(color="#10773e",label = 'Forest'),
        mpatches.Patch(color="#eeefce",label = 'Pasture'),
        mpatches.Patch(color="#e4a540",label = 'Soy/corn'),
        mpatches.Patch(color="#a4507d",label = 'Soy/cotton'),
        mpatches.Patch(color="#c948a2",label = 'Soy/fallow'),
        mpatches.Patch(color="#be5b1d",label = 'Soy/millet'),
        mpatches.Patch(color="#f09cde",label = 'Soy/sunflower'),
        mpatches.Patch(color="#877712",label = 'Sugarcane'),
        mpatches.Patch(color="#614040",label = 'Urban area'),
        mpatches.Patch(color="#1b5ee4",label = 'Water'),
        mpatches.Patch(color="#0cf8c1",label = 'Secondary veg.'),
        mpatches.Patch(color="#00000000",label = 'No data')
]

ax1.set_title('Landuse map original')
ax1.set_xlabel('Column #')
ax1.set_ylabel('Row #')
ax1.legend(handles=legend_landuse1,bbox_to_anchor=(1.05,1), loc=2,
    borderaxespad=0.)
plt.imsave(default_directory +
    "/MatoGrosso_2017_original.tif",
    landuse_original,format='tiff',cmap=cmap1)

# plot reclassified landuse map
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


ax1.set_title('Landuse map original')
ax1.set_xlabel('Column #')
ax1.set_ylabel('Row #')
ax1.legend(handles=legend_landuse2,bbox_to_anchor=(1.05,1), loc=2,
    borderaxespad=0.)
plt.imsave(default_directory +
    "/MatoGrosso_2017_reclass.tif",
    landuse_reclass,format='tiff',cmap=cmap2)
#plt.show()


''''landuse_clipped = landuse_reclass[0:500,0:500]
plt.imsave(default_directory +
    "/MatoGrosso_2017_clipped.tif",
    landuse_clipped,format='tiff')
plt.show()

np.save(default_directory + "/MatoGrosso_2017_clipped.npy",landuse_clipped)
img_reclass = plt.imshow(landuse_clipped, interpolation = "none", cmap = cmap2, vmin = 0.5, vmax = 10.5)
plt.show()''''

"""
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
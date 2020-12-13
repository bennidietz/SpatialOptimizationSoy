import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pickle
import matplotlib.patches as mpatches
from _default_directory import default_directory

# read data from tiff file
landuse_original = plt.imread(default_directory + "/Landuse_maps/mt_2017_v3_1_reprojection.tif")

# plot original landuse map
f1, ax1 = plt.subplots(1)
cmap1 = ListedColormap(["#b3cc33","#be94e8","#10773e","#eeefce",
    "#e4a540","#a4507d","#c948a2","#be5b1d",
    "#f09cde","#877712","#614040","#1b5ee4",
    "#0cf8c1","#00000000","#00000000"])
legend_landuse1 = [mpatches.Patch(color="#b3cc33",label = 'Cerrado'),
mpatches.Patch(color="#be94e8",label = 'Fallow/cotton'),
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
mpatches.Patch(color="#00000000",label = 'No data')]
im1 = plt.imshow(landuse_original,interpolation='none',
cmap=cmap1,vmin = 0.5, vmax = 15.5)
ax1.set_title('Landuse map original')
ax1.set_xlabel('Column #')
ax1.set_ylabel('Row #')
ax1.legend(handles=legend_landuse1,bbox_to_anchor=(1.05, 1), loc=2,
borderaxespad=0.)
plt.imsave(default_directory +
"/Landuse_maps/MatoGrosso_2017_original.tif",
landuse_original,format='tiff',cmap=cmap1)
plt.show()

# create empty map
rows = landuse_original.shape[0]
cols = landuse_original.shape[1]
landuse_reclass = np.zeros((rows,cols),dtype= 'uint8')
# reclassify landuse map
landuse_reclass[landuse_original == 1] = 2
landuse_reclass[landuse_original == 2] = 6
landuse_reclass[landuse_original == 3] = 1
landuse_reclass[landuse_original == 4] = 7
landuse_reclass[landuse_original == 5] = 4
landuse_reclass[landuse_original == 6] = 4
landuse_reclass[landuse_original == 7] = 4
landuse_reclass[landuse_original == 8] = 4
landuse_reclass[landuse_original == 9] = 4
landuse_reclass[landuse_original == 10] = 5
landuse_reclass[landuse_original == 11] = 9
landuse_reclass[landuse_original == 12] = 8
landuse_reclass[landuse_original == 13] = 3
landuse_reclass[landuse_original == 15] = 10

f2, ax2 = plt.subplots(1)
cmap2 = ListedColormap(["#10773e","#b3cc33", "#0cf8c1", "#a4507d",
    "#877712","#be94e8","#eeefce","#1b5ee4",
    "#614040","#00000000"])
legend_landuse2 = [mpatches.Patch(color="#10773e",label = 'Forest'),
mpatches.Patch(color="#b3cc33",label = 'Cerrado'),
mpatches.Patch(color="#0cf8c1",label = 'Secondary vegetation'),
mpatches.Patch(color="#a4507d",label = 'Soy'),
mpatches.Patch(color="#877712",label = 'Sugarcane'),
mpatches.Patch(color="#be94e8",label = 'Fallow/cotton'),
mpatches.Patch(color="#eeefce",label = 'Pasture'),
mpatches.Patch(color="#1b5ee4",label = 'Water'),
mpatches.Patch(color="#614040",label = 'Urban'),
mpatches.Patch(color="#00000000",label = 'No data')]

im2 = plt.imshow(landuse_reclass,interpolation='none',
cmap=cmap2,vmin = 0.5, vmax = 10.5)
ax2.set_title('Landuse map reclass')
ax2.set_xlabel('Column #')
ax2.set_ylabel('Row #')
ax2.legend(handles=legend_landuse2,bbox_to_anchor=(1.05, 1), loc=2,
borderaxespad=0.)
plt.imsave(default_directory +
"/Landuse_maps/MatoGrosso_2017_reclass.tif",
landuse_reclass,format='tiff',cmap=cmap2)
plt.show()

landuse_clipped = landuse_reclass[2800:2900,1700:1800]
np.save(default_directory +
"/Landuse_maps/landuse_map_in.npy",landuse_clipped)

im3 = plt.imshow(landuse_clipped,interpolation='none',
cmap=cmap2,vmin = 0.5, vmax = 10.5)
plt.show()

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

import settings
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pickle
import matplotlib.patches as mpatches

def allClassifiedRastersExist():
    return os.path.isfile(settings.get_file_landuse_reclass()) \
    and os.path.isfile(settings.get_file_reclass_amazon_npy()) and os.path.isfile(settings.get_file_reclass_amazon_tif()) \
    and os.path.isfile(settings.get_file_reclass_cerrado_npy()) and os.path.isfile(settings.get_file_reclass_cerrado_tif())

if os.path.isfile(settings.get_file_landuse()):
    if not allClassifiedRastersExist():
        # read data from tiff file as numpy array
        landuse_original = plt.imread(settings.get_file_landuse())

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
        im1 = plt.imshow(landuse_original, interpolation='none',
        cmap=cmap1,vmin = 0.5, vmax = 15.5)
        ax1.set_title('Landuse map original')
        ax1.set_xlabel('Column #')
        ax1.set_ylabel('Row #')
        ax1.legend(handles=legend_landuse1,bbox_to_anchor=(1.05,1), loc=2,
            borderaxespad=0.)
        plt.imsave(settings.get_file_landuse_colored(),
            landuse_original, format='tiff', cmap=cmap1)

        # plot reclassified landuse map
        f2, ax2 = plt.subplots(1)
        cmap2 = ListedColormap(["#b3cc33","#be94e8","#1b5ee4", "#10773e", "#000000"])
        legend_landuse2 = [
                mpatches.Patch(color="#b3cc33",label = 'Soy'),
                mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
                mpatches.Patch(color="#1b5ee4",label = 'Water'),
                mpatches.Patch(color="#10773e",label = 'Not soy'),
                mpatches.Patch(color="#000000",label = 'No data')
        ]

        cmap3 = ListedColormap(["#b3cc33","#be94e8","#1b5ee4", "#10773e"])
        legend_landuse3 = [
                mpatches.Patch(color="#b3cc33",label = 'Soy'),
                mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
                mpatches.Patch(color="#1b5ee4",label = 'Water'),
                mpatches.Patch(color="#10773e",label = 'Not soy')
        ]

        # create empty map
        rows = landuse_original.shape[0]
        cols = landuse_original.shape[1]
        landuse_reclass = np.zeros((rows,cols),dtype= 'uint8')
        # reclassify landuse map: 1 = soy; 2 = urban area; 3 = water; 4 = not soy; 5 = no data
        landuse_reclass[landuse_original == 1] = 2 # cerrado -> not soy
        landuse_reclass[landuse_original == 2] = 2 # fallow/cotton -> not soy
        landuse_reclass[landuse_original == 3] = 2 # forest -> not soy
        landuse_reclass[landuse_original == 4] = 2 # pasture -> not soy
        landuse_reclass[landuse_original == 5] = 1 # soy/ corn -> soy
        landuse_reclass[landuse_original == 6] = 1 # soy/ cotton -> soy
        landuse_reclass[landuse_original == 7] = 1 # soy/ fallow -> soy
        landuse_reclass[landuse_original == 8] = 1 # soy/ millet -> soy
        landuse_reclass[landuse_original == 9] = 1 # soy/ sunflower -> soy
        landuse_reclass[landuse_original == 10] = 2 # sugarcane -> not soy
        landuse_reclass[landuse_original == 11] = 4 # urban area -> urban area
        landuse_reclass[landuse_original == 12] = 3 # water -> water
        landuse_reclass[landuse_original == 13] = 2 # secondary vegetation -> not soy
        landuse_reclass[landuse_original == 15] = 5 # no data -> no data

        im1 = plt.imshow(landuse_original, interpolation='none',
        cmap=cmap2, vmin = 0.5, vmax = 15.5)
        ax2.set_title('Landuse map reclassified')
        ax2.set_xlabel('Column #')
        ax2.set_ylabel('Row #')
        ax2.legend(handles=legend_landuse3, bbox_to_anchor=(1.05,1), loc=2,
            borderaxespad=0.)
        plt.imsave(settings.get_file_landuse_reclass(), landuse_reclass, format = "tiff", cmap = cmap2)

        amazon_crop = landuse_reclass[900:1500, 600:1600]
        plt.imsave(settings.get_file_reclass_amazon_tif(), amazon_crop, format='tiff', cmap=cmap3)
        settings.printFileCreated(settings.get_file_reclass_amazon_tif())
        np.save(settings.get_file_reclass_amazon_npy(), amazon_crop)
        settings.printFileCreated(settings.get_file_reclass_amazon_npy())

        cerrado_crop = landuse_reclass[3700:4300, 4000:5000]
        plt.imsave(settings.get_file_reclass_cerrado_tif(), cerrado_crop, format='tiff', cmap=cmap3)
        settings.printFileCreated(settings.get_file_reclass_cerrado_tif())
        np.save(settings.get_file_reclass_cerrado_npy(), cerrado_crop)
        settings.printFileCreated(settings.get_file_reclass_cerrado_npy_tif())

        plt.show()
    else:
        print("The reclassified rasters already exists for amazon and cerrado.")
elif allClassifiedRastersExist():
    print("The reclassified rasters already exists for amazon and cerrado.")
else:
    print("To create the classified rasters for amazon and cerado, the file " + settings.getEnding(settings.get_file_landuse()) + " is required.")

if os.path.exists(settings.get_file_soy()):
    if os.path.exists(settings.get_file_soy_amazon()):
        settings.printFileAlreadyExists(settings.get_file_soy_amazon())
    else:
        soy_pot_yield_amazon = np.loadtxt(settings.get_file_soy(), skiprows=6)[900:1500,600:1600]
        with open(settings.get_file_soy_amazon(), 'wb') as output:
            pickle.dump(soy_pot_yield_amazon, output, pickle.HIGHEST_PROTOCOL)
        settings.printFileCreated(settings.get_file_soy_amazon())
    if os.path.exists(settings.get_file_soy_cerrado()):
        settings.printFileAlreadyExists(settings.get_file_soy_cerrado())
    else:
        soy_pot_yield_cerrado = np.loadtxt(settings.get_file_soy(),skiprows=6)[3700:4300,4000:5000]
        with open(settings.get_file_soy_cerrado(), 'wb') as output:
            pickle.dump(soy_pot_yield_cerrado, output, pickle.HIGHEST_PROTOCOL)
        settings.printFileCreated(settings.get_file_soy_cerrado())
elif not os.path.isfile(settings.get_file_soy_amazon()) or not os.path.isfile(settings.get_file_soy_cerrado()):
    print("The file " + settings.getEnding(settings.get_file_soy()) + " is required to generate the data for amazon and cerrado.")

'''
# read potential yield maps from asc file
sugarcane_pot_yield = np.loadtxt(default_directory +
    "/data/Objectives/sugarcane_new.asc",
    skiprows=6)[2800:2900,1700:1800]
cotton_pot_yield = np.loadtxt(default_directory +
    "/data/Objectives/cotton_new.asc",
    skiprows=6)[2800:2900,1700:1800]
pasture_pot_yield = np.loadtxt(default_directory +
    "/data/Objectives/grass_new.asc",
    skiprows=6)[2800:2900,1700:1800]

# save the cropped potential yield maps
with open(default_directory + "/data/Objectives/sugarcane_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(sugarcane_pot_yield, output, pickle.HIGHEST_PROTOCOL)
with open(default_directory + "/data/Objectives/soy_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(soy_pot_yield, output, pickle.HIGHEST_PROTOCOL)
with open(default_directory + "/data/Objectives/cotton_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(cotton_pot_yield, output, pickle.HIGHEST_PROTOCOL)
with open(default_directory + "/data/Objectives/pasture_potential_yield_example.pkl", 'wb') as output:
    pickle.dump(pasture_pot_yield, output, pickle.HIGHEST_PROTOCOL)

plt.imshow(default_directory + "/data/Objectives/soy_potential_yield_example.pkl",interpolation='none',
    cmap=cmap2, vmin = 0.5, vmax = 10.5) '''

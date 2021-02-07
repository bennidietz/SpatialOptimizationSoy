import numpy as np
import os, settings, debugger_helper
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

default_directory = os.path.dirname(os.path.realpath(__file__))

# make initial population for genetic algorithm
def initialize_spatial(pop_size, landuse_map_path):
    all_landusemaps = []
    landuse_map_in = np.load(landuse_map_path)
    rows = landuse_map_in.shape[0]
    cols = landuse_map_in.shape[1]

    # iterate to get multiple realizations for the initial population
    for i in range(1, pop_size+1):
        #use uniform distribution to select 30% of the cells
        landuse_map_ini = np.zeros((rows,cols),dtype='uint8')
        random_map = np.random.uniform(0.0,1.0,(rows,cols))
        random_map_mw = np.zeros((rows,cols))

        print("Iteration " + str(i) + ":")
        print("Initial state: " + str(debugger_helper.getOccurancies(landuse_map_ini)))
        print("Initial state landuse map : " + str(debugger_helper.getOccurancies(landuse_map_in)))

        # take window average of random map to create larger patches
        for x in range(0,cols-1):
            for y in range(0,rows-1):
                if x == 0 or y == 0 or x == cols-1 or y == rows-1:
                    random_map_mw[y,x] = 1.0
                else:
                    random_map_mw[y,x] = random_map[y-1:y+2,x-1:x+2].mean()

        # 70% of the map remains the current land use
        landuse_map_ini = np.where(random_map_mw>=0.3,
                            landuse_map_in,landuse_map_ini)
        print("After letting 70% of cells remain : " + str(debugger_helper.getOccurancies(landuse_map_ini)))
        # 30% of the map will become new
        # urban, water and no data will remain the same
        # reclassify landuse map: 1 = soy; 2 = not soy; 3 = water; 4 = urban area; 5 = no data
        landuse_map_ini = np.where(landuse_map_in >= 3,
                            landuse_map_in,landuse_map_ini)
        print("After letting 30% of become new : " + str(debugger_helper.getOccurancies(landuse_map_ini)))
        # other land use classes can change into 1 or 2
        # choose which land cover type
        landuse_map_ini = np.where(landuse_map_ini == 0,
                        np.random.randint(low=1, high=3,size=(rows,cols)),
                        landuse_map_ini)
        print("After transfer others on 1 and 2: " + str(debugger_helper.getOccurancies(landuse_map_ini)))
        all_landusemaps.append(landuse_map_ini)
    return np.array(all_landusemaps)

'''maps = initialize_spatial(3, settings.get_file_reclass_amazon_npy())
f, axes = plt.subplots(1,3)

cmap = ListedColormap(["#b3cc33","#be94e8","#1b5ee4", "#10773e"])
for amap, ax in zip(maps, axes):
    im = ax.imshow(amap,interpolation='none', cmap=cmap,vmin = 0.5, vmax = 4.5)
plt.colorbar(im, orientation='horizontal')
plt.show()'''

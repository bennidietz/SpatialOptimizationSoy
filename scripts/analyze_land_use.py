import initial_population
import numpy as np
import os, settings, debugger_helper
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def analyze_land_use_configuration(area, pop_size):
    if area == 'amazon':
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_amazon_npy())
    else:
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_cerrado_npy())

    f, axes = plt.subplots(1, 3)

    cmap = ListedColormap(["#b3cc33", "#10773e", "#be94e8", "#1b5ee4"])

    for amap, ax in zip(maps, axes):
        im = ax.imshow(amap, interpolation = 'none', cmap = cmap, vmin = 0.5, vmax = 4.5)

    plt.colorbar(im, orientation = 'horizontal')
    plt.suptitle('Land use configuration ' + area + ' (population size: ' + str(pop_size) + ')')
    plt.show()

def compare_land_use(mapA, mapB):

    if mapA.shape != mapB.shape:
        return []

    output = np.zeros(mapA.shape)

    for i in range(mapA.shape[0]):
        for k in range(mapA.shape[1]):
            #changed from not soy to soy
            if mapA[i][k] == 2 and mapB[i][k] == 1:
                output[i][k] = 1
            #changed from soy to not soy
            elif mapA[i][k] == 1 and mapB[i][k] == 2:
                output[i][k] = 2
            #could not change
            elif mapA[i][k] == 3 or mapA[i][k] == 4:
                output[i][k] = 4
            #could have changed but didnt
            else:
                output[i][k] = 3

    return output

def analyze_land_use_change(area, pop_size):
    if area == 'amazon':
        initial_map = np.load(settings.get_file_reclass_amazon_npy())
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_amazon_npy())
    else:
        initial_map = np.load(settings.get_file_reclass_cerrado_npy())
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_cerrado_npy())

    i = 1

    for map in maps:
        cmap = ListedColormap(["#b3cc33", "#10773e", "#999999", "#777777"])

        im = plt.imshow(compare_land_use(initial_map, map), interpolation = 'none', cmap = cmap, vmin = 0.5, vmax = 4.5)

        plt.colorbar(im, orientation = 'horizontal')
        plt.suptitle('Land use change ' + area + ' (population size: ' + str(i) + ')')
        plt.show()

        i += 1

#analyze_land_use_configuration('amazon', 3)
#analyze_land_use_configuration('cerrado', 3)

analyze_land_use_change('amazon', 1)
analyze_land_use_change('cerrado', 1)

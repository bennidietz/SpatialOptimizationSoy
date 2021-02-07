import initial_population
import numpy as np
import os, settings, debugger_helper
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

def analyze_land_use_configuration(area, pop_size):
    if area == 'amazon':
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_amazon_npy())
    else:
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_cerrado_npy())

    f, axes = plt.subplots(1, len(maps))

    cmap = ListedColormap(["#b3cc33", "#10773e", "#be94e8", "#1b5ee4"])

    if len(maps) > 1:
        for amap, ax in zip(maps, axes):
            im = ax.imshow(amap, interpolation = 'none', cmap = cmap, vmin = 0.5, vmax = 4.5)
    else:
        im = axes.imshow(maps[0], interpolation = 'none', cmap = cmap, vmin = 0.5, vmax = 4.5)

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
                continue

            #changed from soy to not soy
            if mapA[i][k] == 1 and mapB[i][k] == 2:
                output[i][k] = 2
                continue

            #could not change
            if mapA[i][k] == 3 or mapA[i][k] == 4:
                output[i][k] = 4
                continue

            #could have changed but didnt
            if mapA[i][k] == mapB[i][k]:
                output[i][k] = 3
                continue

            #algorithm failure
            output[i][k] = 5

    return output

def print_land_use_change(map, title = 'Land use change'):
    cmap = ListedColormap(["#b3cc33", "#10773e", "#999999", "#777777", "#e30000"])
    legend_landuse = [
            mpatches.Patch(color="#b3cc33", label = 'Changed from not soy to soy'),
            mpatches.Patch(color="#10773e", label = 'Changed from soy to not soy'),
            mpatches.Patch(color="#999999", label = 'Did not change'),
            mpatches.Patch(color="#777777", label = 'Could not change'),
            mpatches.Patch(color="#e30000", label = 'Algorithm failure'),
    ]

    im = plt.imshow(map, interpolation = 'none', cmap = cmap, vmin = 0.5, vmax = 5.5)

    plt.suptitle('Land use change')
    plt.legend(handles = legend_landuse, bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0.)
    plt.show()

def analyze_land_use_change(area, pop_size):
    if area == 'amazon':
        initial_map = np.load(settings.get_file_reclass_amazon_npy())
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_amazon_npy())
    else:
        initial_map = np.load(settings.get_file_reclass_cerrado_npy())
        maps = initial_population.initialize_spatial(pop_size, settings.get_file_reclass_cerrado_npy())

    i = 1

    for map in maps:
        print_land_use_change(compare_land_use(initial_map, map), 'Land use change ' + area + ' (population size: ' + str(i) + ')')

        i += 1

#analyze_land_use_configuration('amazon', 3)
#analyze_land_use_configuration('cerrado', 3)

#analyze_land_use_change('amazon', 1)
#analyze_land_use_change('cerrado', 1)

import initial_population
import numpy as np
import os, settings, debugger_helper
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

maps = initial_population.initialize_spatial(3, settings.get_file_reclass_amazon_npy())
f, axes = plt.subplots(1, 3)

cmap = ListedColormap(["#b3cc33", "#10773e", "#be94e8", "#1b5ee4"])

for amap, ax in zip(maps, axes):
    im = ax.imshow(amap,interpolation='none', cmap=cmap, vmin = 0.5, vmax = 4.5)

plt.colorbar(im, orientation='horizontal')
plt.show()

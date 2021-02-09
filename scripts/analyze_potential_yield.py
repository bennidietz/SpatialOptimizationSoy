import initial_population
import numpy as np
#import pickle5 as pickle
import os, settings, debugger_helper
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib.cm as cm

def analyze_yield(map, title = 'Potential yield'):
    cmap = clr.LinearSegmentedColormap.from_list('custom green', ['#61ff33', '#208901'], N = 10)
    normalize = clr.Normalize(vmin = map.min(), vmax = map.max())
    scalarmappaple = cm.ScalarMappable(norm = normalize, cmap = cmap)
    scalarmappaple.set_array(map)
    plt.imshow(map, extent = (0, len(map), 0, len(map)), origin = 'lower', cmap = cmap)
    plt.colorbar(scalarmappaple)
    plt.title(title)
    plt.show()

analyze_yield(np.load(settings.get_file_prec_amazon_interpolated()), 'Potential yield amazon')
analyze_yield(np.load(settings.get_file_prec_cerrado_interpolated()), 'Potential yield cerrado')

#with open(settings.get_file_soy_amazon(), 'rb') as file:
    #potential_yield_amazon = pickle.load(file)

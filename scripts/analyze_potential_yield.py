#only works in python 3.7

import initial_population
import numpy as np
import pickle5
import os, settings, debugger_helper
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

def analyze_yield(map, printResults = False):
    print(1)

#analyze_yield(pickle.load(open(settings.get_file_soy_amazon())), True)
#analyze_yield(np.load(settings.get_file_soy_cerrado(), allow_pickle = True), True)

with open(settings.get_file_soy_amazon(), 'rb') as file:
    potential_yield_amazon = pickle5.load(file)

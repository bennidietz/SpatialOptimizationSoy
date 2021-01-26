import os, settings

default_directory = os.path.dirname(os.path.realpath(__file__))

import numpy as np
from external import compute_genome
import pickle5 as pickle
import math as m
import csv
import pandas as pd

# calculate soy yield of landuse
def calc_soy_yield(realizations,soy_map,area):
    soyYield = []

    # loop over the individuals in the population
    for land_use_map in realizations:
        soy_yield = np.where(land_use_map == 1, soy_map*area, 0)
        # all soy yield
        soyYield.append(np.sum(soy_yield))

    output = np.array(soyYield)
    return(output)

# read clipped land use
amazon_landuse = np.load(settings.get_file_reclass_amazon_npy())
cerrado_landuse = np.load(settings.get_file_reclass_cerrado_npy())
cellArea = 6.25
amazon_landuse = [amazon_landuse]
cerrado_landuse = [cerrado_landuse]

def calculate_water_footprint(realization, soy_map, prec_data, area):
    soyYieldArray = calc_soy_yield(realization, soy_map, area)
    waterfootprints = []
    #print("In calculation of water footprint soy_yield has length " + str(len(soy_yield)))
    # Calculate evaporation
    for soy_yield in soyYieldArray:
        waterEvaporation = []
        for row in prec_data:
            value = row * 20 /100
            waterEvaporation.append(value)
        
        # Calculating waterincorporation 
        soy_yieldGram = soy_yield * 1000000 # calculating tons in gram
        waterIncGram = soy_yieldGram * 0.085 # gram * amount of water
        waterInc = waterIncGram / 1000000 # convert gram to tons

        # Calculating the green waterfootprint: Evaporation + waterincorporation
        EvWI = []
        for i in waterEvaporation:
            value2 = i + waterInc
            EvWI.append(value2)

        # Sum values in array for the green waterfootprint
        greenWF = np.sum(EvWI)

        ######## For calculating the blue water footprint
        ## Precipitation divided with 2 for the lost return flow
        lostRF = []
        for row in prec_data:
            lostreturnflow = row / 2
            lostRF.append(lostreturnflow)
        lostReturnFlow = np.sum(lostRF)
        blueWF = greenWF + lostReturnFlow
        waterfootprints.append(np.sum(blueWF + greenWF))

    return np.array(waterfootprints)

# # read input data for objectives
# with open(default_directory + "/Objectives/sugarcane_potential_yield_example.pkl", 'rb') as output:
#    sugarcane_pot_yield = pickle.load(output)

'''with open(settings.get_file_soy_amazon(), 'rb') as output:
    print(settings.get_file_soy_amazon())
    soy_pot_yield = pickle.load(output)
    prec_amazon = np.load(settings.get_file_prec_amazon_interpolated())
    temp_amazon = np.load(settings.get_file_temp_amazon_interpolated())
    yields_test =  calc_soy_yield(amazon_landuse, soy_pot_yield, cellArea)
    waterfootprint_test =  calculate_water_footprint(amazon_landuse, soy_pot_yield, prec_amazon, cellArea)
    print("Amazon crop - total yield: " + str(yields_test))
    print("Amazon crop - water footprint: " + str(waterfootprint_test))'''
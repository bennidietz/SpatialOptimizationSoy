import os, settings

default_directory = os.path.dirname(os.path.realpath(__file__))

import numpy as np
from external import compute_genome
import pickle

# calculate soy yield of landuse
def calc_soy_yield(landuse_map,soy_map,area):
    soyYield = []

    # loop over the individuals in the population
    for land_use_map in landuse_map:
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

def calculate_water_footprint(landuse_map, soy_map, prec_data, temp_data, area):
    soy_yield = calc_soy_yield(landuse_map, soy_map, area)[0]
    return

def calculate_above_ground_biomass(landuse_map_in,area): 
    # loop over the individuals in the population
    all_emissions = []

    for land_use_map in landuse_map_in:
        # calculate the total area of each land use class
        forest_area = np.count_nonzero(land_use_map == 1)*area
        cerrado_area = np.count_nonzero(land_use_map == 2)*area
        secondary_vegetation_area = np.count_nonzero(land_use_map == 3)*area
        soy_area = np.count_nonzero(land_use_map == 4)*area
        sugarcane_area = np.count_nonzero(land_use_map == 5)*area

        pasture_area = np.count_nonzero(land_use_map == 7)*area

        # multiply area of the land use class (ha) with the AGB (tonnes/ha)
        agb_forest = forest_area*300
        agb_cerrado = cerrado_area*48
        agb_secondary_vegetation = secondary_vegetation_area*150
        agb_soy = soy_area*0
        agb_surgarcane = sugarcane_area*16

        agb_pasture = pasture_area*6.7*0.7


        # sum over all land use classes
        above_ground_biomass_all = agb_forest + agb_cerrado + agb_secondary_vegetation + agb_soy + agb_surgarcane + agb_pasture
        # add to the array with all individuals
        all_emissions.append(above_ground_biomass_all)

    return(np.array(all_emissions))

# read input data for objectives
with open(settings.get_file_soy_amazon(), 'rb') as output:
    prec_amazon = np.load(settings.get_file_prec_amazon_interpolated())
    temp_amazon = np.load(settings.get_file_temp_amazon_interpolated())
    soy_pot_yield = pickle.load(output)
    yields_test =  calc_soy_yield(amazon_landuse, soy_pot_yield, cellArea)
    waterfootprint_test =  calculate_water_footprint(amazon_landuse, soy_pot_yield, prec_amazon, temp_amazon, cellArea)
    print("Amazon crop - total yield: " + str(yields_test))
    print("Amazon crop - water footprint: " + str(waterfootprint_test))
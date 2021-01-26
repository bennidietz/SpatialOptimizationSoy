import numpy as np
import pickle, os
from compute_genome import create_patch_ID_map
default_directory = os.path.dirname(os.path.realpath(__file__)) + "/.."

# calculate the total yield for sugarcane, soy, cotton and pasture
def calculate_tot_yield(landuse_map_in, sugarcane_map,soy_map,cotton_map,
    pasture_map,cellarea):
    all_yields = []
    # loop over the individuals in the population
    for land_use_map in landuse_map_in:
        #sugarcane
        yield_sugarcane = np.where(land_use_map == 5, sugarcane_map*cellarea, 0)
        tot_yield_sugarcane = np.sum(yield_sugarcane)
        # soy
        yield_soy = np.where(land_use_map == 4, soy_map*cellarea, 0)
        tot_yield_soy = np.sum(yield_soy)
        #cotton
        yield_cotton = np.where(land_use_map == 6, cotton_map*cellarea, 0)
        tot_yield_cotton = np.sum(yield_cotton)
        #pasture
        yield_pasture = np.where(land_use_map == 7, pasture_map*cellarea, 0)
        tot_yield_pasture = np.sum(yield_pasture)

        # total yield agriculture is equal to sum of different crops
        tot_yield = tot_yield_soy + tot_yield_sugarcane + tot_yield_cotton + tot_yield_pasture
        all_yields.append(tot_yield)

    return(np.array(all_yields))

# read clipped land use
landuse = np.load(default_directory + "/Landuse_maps/landuse_map_in.npy")
landuse = [landuse]
#print(np.shape(landuse))
# read input data for objectives
with open(default_directory + "/Objectives/sugarcane_potential_yield_example.pkl", 'rb') as output:
    sugarcane_pot_yield = pickle.load(output)
with open(default_directory + "/Objectives/soy_potential_yield_example.pkl", 'rb') as output:
    soy_pot_yield = pickle.load(output)
with open(default_directory + "/Objectives/cotton_potential_yield_example.pkl", 'rb') as output:
    cotton_pot_yield = pickle.load(output)
with open(default_directory + "/Objectives/pasture_potential_yield_example.pkl", 'rb') as output:
    pasture_pot_yield = pickle.load(output)

totalYield = calculate_tot_yield(landuse, sugarcane_pot_yield, soy_pot_yield, cotton_pot_yield, pasture_pot_yield, 6.25)
#print(totalYield)

def calculate_above_ground_biomass(landuse_map_in,cellarea):
    # loop over the individuals in the population
    all_emissions = []
    for land_use_map in landuse_map_in:
        # calculate the total area of each land use class
        forest_area = np.count_nonzero(land_use_map == 1)*cellarea
        cerrado_area = np.count_nonzero(land_use_map == 2)*cellarea
        secondary_vegetation_area = np.count_nonzero(land_use_map == 3)*cellarea
        sugarcane_area = np.count_nonzero(land_use_map == 5)*cellarea
        pasture_area = np.count_nonzero(land_use_map == 7)*cellarea
        # multiply area of the land use class (ha) with the AGB (tonnes/ha)
        agb_forest = forest_area*300
        agb_cerrado = cerrado_area*48
        agb_secondary_vegetation = secondary_vegetation_area*150
        agb_sugarcane = sugarcane_area*16
        agb_pasture = pasture_area*6.7*0.7
        # sum over all land use classes
        above_ground_biomass_all = agb_forest + agb_cerrado + agb_secondary_vegetation + agb_sugarcane + agb_pasture
        # add to the array with all individuals
        all_emissions.append(above_ground_biomass_all)

    return(np.array(all_emissions))

biomass = calculate_above_ground_biomass(landuse, 6.25)
#print(biomass)

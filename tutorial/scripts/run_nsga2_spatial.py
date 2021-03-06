from pymoo import factory
from pymoo.model.crossover import Crossover
import spatial_extention_pymoo

# add spatial functions to pymoo library
factory.get_sampling_options = spatial_extention_pymoo._new_get_sampling_options
factory.get_crossover_options = spatial_extention_pymoo._new_get_crossover_options
factory.get_mutation_options = spatial_extention_pymoo._new_get_mutation_options
Crossover.do = spatial_extention_pymoo._new_crossover_do

import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pymoo.util.misc import stack
from pymoo.model.problem import Problem
from calculate_objectives import calculate_tot_yield, calculate_above_ground_biomass
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.factory import get_termination
from pymoo.optimize import minimize
import os
default_directory = os.path.dirname(os.path.realpath(__file__)) + "/.."

cell_area = 2.5 * 2.5 # in hectares

# read input data for objectives
with open(default_directory + "/Objectives/sugarcane_potential_yield_example.pkl", 'rb') as output:
    sugarcane_pot_yield = pickle.load(output)
with open(default_directory + "/Objectives/soy_potential_yield_example.pkl", 'rb') as output:
    soy_pot_yield = pickle.load(output)
with open(default_directory + "/Objectives/cotton_potential_yield_example.pkl", 'rb') as output:
    cotton_pot_yield = pickle.load(output)
with open(default_directory + "/Objectives/pasture_potential_yield_example.pkl", 'rb') as output:
    pasture_pot_yield = pickle.load(output)

class MyProblem(Problem):

    def __init__(self):
        super().__init__(n_var=100,
                         n_obj=2,
                         n_constr=0,
                         xl=0.0,
                         xu=1.0)

    # define the objective functions
    def _evaluate(self, X, out, *args, **kwargs):
        f1 = -calculate_tot_yield(X[:], sugarcane_pot_yield,soy_pot_yield, cotton_pot_yield,pasture_pot_yield,cell_area)
        f2 = -calculate_above_ground_biomass(X[:],cell_area)
        out["F"] = np.column_stack([f1, f2])

problem = MyProblem()
print(problem)

#algorithm

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation

algorithm = NSGA2(
    pop_size=70,
    n_offsprings=10,
    sampling=get_sampling("spatial", default_dir = default_directory),
    crossover=get_crossover("spatial_one_point_crossover", n_points = 3),
    mutation=get_mutation("spatial_n_point_mutation", prob = 0.01,
    point_mutation_probability = 0.015),
    eliminate_duplicates=False
)

#termination

from pymoo.factory import get_termination

termination = get_termination("n_gen", 50)

#optimization

from pymoo.optimize import minimize
res = minimize(problem,
    algorithm,
    termination,
    seed=1,
    save_history=True,
    verbose=True)

print(res)
print(res.X)
print(res.F)

#visualization

f1, ax1 = plt.subplots(1)
im1 = plt.scatter(-res.F[:,0],-res.F[:,1])
ax1.set_title("Objective Space")
ax1.set_xlabel('Total yield [tonnes]')
ax1.set_ylabel('Above ground biomass [tonnes]')
plt.show()

import matplotlib.patches as mpatches
# define the colors of the land use classes
cmap = ListedColormap(["#10773e","#b3cc33", "#0cf8c1", "#a4507d","#877712","#be94e8","#eeefce","#1b5ee4","#614040","#00000000"])

# build a legend with these colors and their land use label
legend_landuse = [mpatches.Patch(color="#10773e", label = 'Forest'),
mpatches.Patch(color="#b3cc33", label = 'Cerrado'),
mpatches.Patch(color="#0cf8c1", label = 'Secondary vegetation'),
mpatches.Patch(color="#a4507d", label = 'Soy'),
mpatches.Patch(color="#877712", label = 'Sugarcane'),
mpatches.Patch(color="#be94e8", label = 'Fallow/cotton'),
mpatches.Patch(color="#eeefce", label = 'Pasture'),
mpatches.Patch(color="#1b5ee4", label = 'Water'),
mpatches.Patch(color="#614040", label = 'Urban'),
mpatches.Patch(color="#00000000", label = 'No data')]
# fetch the two extremes of the Pareto front from res.X
landuse_max_yield = res.X[np.argmax(-res.F[:,0], axis=0)]
landuse_max_biomass = res.X[np.argmax(-res.F[:,1], axis=0)]
# Plot them next to each other
f2, (ax2a, ax2b) = plt.subplots(1,2, figsize=(9,5))
im2a = ax2a.imshow(landuse_max_yield,interpolation='None',
cmap=cmap,vmin=0.5,vmax=10.5)
ax2a.set_title('Landuse map \nmaximized total yield', fontsize=10)
ax2a.set_xlabel('Column #')
ax2a.set_ylabel('Row #')
im2b = ax2b.imshow(landuse_max_biomass,interpolation='None',
cmap=cmap,vmin=0.5,vmax=10.5)
ax2b.set_title('Landuse map \nminimized CO2 emissions', fontsize=10)
ax2b.set_xlabel('Column #')
plt.legend(handles=legend_landuse,bbox_to_anchor=(1.05, 1), loc=2,
prop={'size': 9})
# Adjust location of the plots to make space for legend and save
plt.subplots_adjust(right = 0.6, hspace=0.2)
plt.savefig(default_directory+"/landuse_max.png",dpi=150)
plt.show()

# create an empty list to save objective values per generation
f = []
# iterate over the generations
for generation in res.history:
    # retrieve the optima for all objectives from the generation
    opt = generation.opt
    this_f = opt.get("F")
    f.append(this_f)
n_gen = np.array(range(1,len(f)+1))
print(n_gen)

# get maximum (extremes) of each generation for both objectives
obj_1 = []
obj_2 = []
for i in f:
    max_obj_1 = min(i[:,0])
    max_obj_2 = min(i[:,1])

    obj_1.append(max_obj_1)
    obj_2.append(max_obj_2)

# visualize the maxima against the generation number
f3, (ax3a, ax3b) = plt.subplots(1,2, figsize=(9,5))
ax3a.plot(n_gen, -np.array(obj_1))
ax3a.set_xlabel("Generation")
ax3a.set_ylabel("Maximum total yield [tonnes]")
ax3b.plot(n_gen, -np.array(obj_2))
ax3b.set_xlabel("Generation")
ax3b.set_ylabel("Above ground biomass [tonnes]")
plt.savefig(default_directory+"/figures/objectives_over_generations")
plt.show()

# add here the generations you want to see in the plot
generations2plot = [10,20,30,40,50]
# make the plot
fig4, ax4 = plt.subplots(1)
# i - 1, because generation 1 has index 0
for i in generations2plot:
    plt.scatter(-f[i-1][:,0],-f[i-1][:,1])
ax4.set_xlabel('Total yield [tonnes]')
ax4.set_ylabel('Above ground biomass [tonnes]')
plt.legend(list(map(str, generations2plot)))
plt.savefig(default_directory+"/figures/pareto_front_over_generations.png")
plt.show()

from pymoo.performance_indicator.hv import Hypervolume
# make an array of the generation numbers
n_gen = np.array(range(1,len(f)+1))
# set reference point
ref_point = np.array([0.0, 0.0])
# create the performance indicator object with reference point
metric = Hypervolume(ref_point=ref_point, normalize=False)
# calculate for each generation the HV metric
hv = [metric.calc(i) for i in f]
# visualze the convergence curve
fig5, ax5 = plt.subplots(1)
ax5.plot(n_gen, hv, '-o', markersize=4, linewidth=2)
ax5.set_xlabel("Generation")
ax5.set_ylabel("Hypervolume")
plt.savefig(default_directory+"/figures/hypervolume.png")
plt.show()

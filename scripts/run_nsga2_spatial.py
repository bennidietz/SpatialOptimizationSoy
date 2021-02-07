from pymoo import factory
from pymoo.model.crossover import Crossover
import spatial_extention_pymoo
import settings
import matplotlib.patches as mpatches

# add spatial functions to pymoo library
factory.get_sampling_options = spatial_extention_pymoo._new_get_sampling_options
factory.get_crossover_options = spatial_extention_pymoo._new_get_crossover_options
factory.get_mutation_options = spatial_extention_pymoo._new_get_mutation_options
Crossover.do = spatial_extention_pymoo._new_crossover_do

import numpy as np
from pickle5 import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pymoo.util.misc import stack
from pymoo.model.problem import Problem
import objectives
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.factory import get_termination
from pymoo.optimize import minimize

cell_area = 2.5 * 2.5 # in hectares

# read input data for objectives
# TODO: do for both amazon and cerrado
with open(settings.get_file_soy_amazon(), 'rb') as output:
    soy_pot_yield = pickle.load(output)

prec_amazon = np.load(settings.get_file_prec_amazon_interpolated())
temp_amazon = np.load(settings.get_file_temp_amazon_interpolated())
prec_cerrado = np.load(settings.get_file_prec_cerrado_interpolated())
temp_cerrado = np.load(settings.get_file_temp_cerrado_interpolated())

class MyProblem(Problem):

    def __init__(self, current_soy_yield):
        self.current_soy_yield = current_soy_yield
        super().__init__(n_var=400,
                         n_obj=2,
                         n_constr=1,
                         xl=0.0,
                         xu=1.0)


    # define the objective functions
    def _evaluate(self, X, out, *args, **kwargs):
        f1 = -objectives.calc_soy_yield(X[:], soy_pot_yield, cell_area) # soy yield will be maximized
        f2 = objectives.calculate_water_footprint(X[:],soy_pot_yield, prec_amazon, cell_area) # water footprint will be minizied

        # soy yield should be above 76154 / 2 = 38077 Tonnes
        g1 =  -f2+self.current_soy_yield/2
        # soy yield should be below 76154 * 2 = 152308 Tonnes
        #g2 =  objectives.calculate_water_footprint(X[:],soy_pot_yield, prec_amazon, cell_area)-self.current_soy_yield*2
        out["F"] = np.column_stack([f1, f2])
        out["G"] = np.column_stack([g1])

#algorithm

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation

algorithm_amazon = NSGA2(
    pop_size=70,
    n_offsprings=10,
    sampling=get_sampling("spatial", landuseData=settings.get_file_reclass_amazon_npy()),
    crossover=get_crossover("spatial_one_point_crossover", n_points = 3),
    mutation=get_mutation("spatial_n_point_mutation", prob = 0.01,
    point_mutation_probability = 0.015),
    eliminate_duplicates=False
)

algorithm_cerrado = NSGA2(
    pop_size=70,
    n_offsprings=10,
    sampling=get_sampling("spatial", landuseData=settings.get_file_reclass_cerrado_npy()),
    crossover=get_crossover("spatial_one_point_crossover", n_points = 3),
    mutation=get_mutation("spatial_n_point_mutation", prob = 0.01,
    point_mutation_probability = 0.015),
    eliminate_duplicates=False
)

#termination

from pymoo.factory import get_termination

termination = get_termination("n_gen", 10)

#optimization
from pymoo.optimize import minimize
res_amazon = minimize(MyProblem(76154.6),
    algorithm_amazon,
    termination,
    seed=1,
    save_history=True,
    verbose=True)

res_cerrado = minimize(MyProblem(578897.6),
    algorithm_cerrado,
    termination,
    seed=1,
    save_history=True,
    verbose=True)


def plot_objective_space(minimizationResults):
    f1, ax1 = plt.subplots(1)
    im1 = plt.scatter(-minimizationResults.F[:,0], minimizationResults.F[:,1])
    ax1.set_title("Objective Space")
    ax1.set_xlabel('Total yield [tonnes]')
    ax1.set_ylabel('Water footprint [m^3/Tonnes]')
    plt.show()

#plot_objective_space(res_cerrado)

#visualization

def plot_design_objective_space(res, name):
    # Plot the design space
    f1, ax1 = plt.subplots(1)
    ax1.scatter(-res.X[:,0], res.X[:,1], s=30, fc='none', ec='r')
    ax1.set_title('design space')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_xlim(-5, 0)
    ax1.set_ylim(0, 7)
    f1.savefig('design_space_' + name + '.png')
    # Plot the objective space
    f2, ax2 = plt.subplots(1)
    ax2.scatter(-res.F[:,0], res.F[:,1], s=30, fc='none', ec='k')
    ax2.set_title('objective space')
    ax2.set_xlabel('f1')
    ax2.set_ylabel('f2')
    f2.savefig('objective_space_' + name + '.png')

def plot_landuse_configuration(minimizationResults, regionName):
    # define the colors of the land use classes
    cmap = ListedColormap(["#b3cc33","#10773e", "#be94e8","#1b5ee4"])

    # build a legend with these colors and their land use label
    legend_landuse = [
        mpatches.Patch(color="#b3cc33",label = 'Soy'),
        mpatches.Patch(color="#10773e",label = 'Not soy'),
        mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
        mpatches.Patch(color="#1b5ee4",label = 'Water')
    ]
    # fetch the two extremes of the Pareto front from res.X
    landuse_max_yield = minimizationResults.X[np.argmax(-minimizationResults.F[:,0], axis=0)]
    landuse_min_waterfootprint = minimizationResults.X[np.argmax(minimizationResults.F[:,1], axis=0)]
    # Plot them next to each other
    f2, (ax2a, ax2b) = plt.subplots(1,2, figsize=(9,5))
    im2a = ax2a.imshow(landuse_max_yield,interpolation='None',
    cmap=cmap,vmin=0.5,vmax=4.5)
    ax2a.set_title(regionName + ': Landuse map \nmaximized total yield', fontsize=10)
    ax2a.set_xlabel('Column #')
    ax2a.set_ylabel('Row #')
    im2b = ax2b.imshow(landuse_min_waterfootprint,interpolation='None',
    cmap=cmap,vmin=0.5,vmax=4.5)
    ax2b.set_title(regionName + ': Landuse map \nminimized water footprint', fontsize=10)
    ax2b.set_xlabel('Column #')
    plt.legend(handles=legend_landuse,bbox_to_anchor=(1.05, 1), loc=2,
    prop={'size': 9})
    # Adjust location of the plots to make space for legend and save
    plt.subplots_adjust(right = 0.6, hspace=0.2)
    plt.savefig(settings.get_default_directory()+"/landuse_max_" + regionName + ".png",dpi=150)
    plt.show()

def plot_config_alternative_colors(minimizationResults, regionName):
    
    # define the colors of the land use classes
    cmap = ListedColormap(["#b3cc33","#10773e","#000000","#1b5ee4","#be94e8"])
    legend_landuse = [
            mpatches.Patch(color="#b3cc33",label = 'Soy'),
            mpatches.Patch(color="#10773e",label = 'Not soy'),
            mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
            mpatches.Patch(color="#1b5ee4",label = 'Water'),
            mpatches.Patch(color="#000000",label = 'No data')
    ]
    # fetch the two extremes of the Pareto front from res.X
    landuse_max_yield = minimizationResults.X[np.argmax(-minimizationResults.F[:,0], axis=0)]
    landuse_min_waterfootprint = minimizationResults.X[np.argmax(minimizationResults.F[:,1], axis=0)]
    # Plot them next to each other
    f2, (ax2a, ax2b) = plt.subplots(1,2, figsize=(9,5))
    im2a = ax2a.imshow(landuse_max_yield,interpolation='None',
    cmap=cmap,vmin=0.5,vmax=4.5)
    ax2a.set_title(regionName + ': Landuse map \nmaximized total yield', fontsize=10)
    ax2a.set_xlabel('Column #')
    ax2a.set_ylabel('Row #')
    im2b = ax2b.imshow(landuse_min_waterfootprint,interpolation='None',
    cmap=cmap,vmin=0.5,vmax=4.5)
    ax2b.set_title(regionName + ': Landuse map \nminimized water footprint', fontsize=10)
    ax2b.set_xlabel('Column #')
    plt.legend(handles=legend_landuse,bbox_to_anchor=(1.05, 1), loc=2,
    prop={'size': 9})
    # Adjust location of the plots to make space for legend and save
    plt.subplots_adjust(right = 0.6, hspace=0.2)
    plt.savefig(settings.get_default_directory()+"/landuse_max_" + regionName + ".png",dpi=150)
    plt.show()


def objectives_per_generation(res, regionName):
    '''
    plot objective values over generation and pareto front
    '''
    f = []
    # iterate over the generations
    for generation in res.history:
        # retrieve the optima for all objectives from the generation
        opt = generation.opt
        this_f = opt.get("F")
        f.append(this_f)
    n_gen = np.array(range(1,len(f)+1))
    print("Objective values per generation for " + regionName + ":")
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
    ax3b.plot(n_gen, np.array(obj_2))
    ax3b.set_xlabel("Generation")
    ax3b.set_ylabel("Water footprint [tonnes]")
    plt.savefig(settings.get_default_directory() + "/objectives_over_generations_" + regionName)
    plt.show()

    # add here the generations you want to see in the plot
    generations2plot = [1,2,3]
    #generations2plot = [10,20,30,40,50]

    # make the plot
    fig4, ax4 = plt.subplots(1)
    # i - 1, because generation 1 has index 0
    for i in generations2plot:
        plt.scatter(-f[i-1][:,0],f[i-1][:,1])
    ax4.set_xlabel('Total yield [tonnes]')
    ax4.set_ylabel('Water footprint [tonnes]')
    plt.legend(list(map(str, generations2plot)))
    plt.savefig(settings.get_default_directory() + "/pareto_front_over_generations_" + regionName + ".png")
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
    plt.savefig(settings.get_default_directory() + "/hypervolume_" + regionName + ".png")
    plt.show()

plot_design_objective_space(res_amazon, "amazon")
plot_landuse_configuration(res_amazon, "amazon")
#plot_landuse_configuration(res_cerrado, "cerrado")
objectives_per_generation(res_amazon, "amazon")
#objectives_per_generation(res_cerrado, "cerrado")
print("1")
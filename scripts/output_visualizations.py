import numpy as np
from analyze_land_use import compare_land_use, print_land_use_change
import settings
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def plot_objective_space(minimizationResults, regionName, unit_wf):
    f1, ax1 = plt.subplots(1)
    im1 = plt.scatter(-minimizationResults.F[:,0], minimizationResults.F[:,1])
    ax1.set_title(regionName + ": Objective Space")
    ax1.set_xlabel('Total yield [tonnes]')
    ax1.set_ylabel('Water footprint ' + unit_wf)
    plt.show()

#plot_objective_space(res_cerrado)

#visualization

def plot_design_objective_space(landuse_results, objective_results, name, unit_wf):
    # Plot the design space
    f1, ax1 = plt.subplots(1)
    ax1.scatter(-landuse_results[:,0], landuse_results[:,1], s=30, fc='none', ec='r')
    ax1.set_title(name + ': design space')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_xlim(-5, 2)
    ax1.set_ylim(-2, 6)
    f1.savefig(name + ': design_space_' + name + '.png')
    # Plot the objective space
    f2, ax2 = plt.subplots(1)
    ax2.scatter(-objective_results[:,0], objective_results[:,1], s=30, fc='none', ec='k')
    ax2.set_title(name + ': objective space')
    ax2.set_xlabel('Soy yield [tonnes]')
    ax2.set_ylabel('Water footprint ' + unit_wf)
    f2.savefig('objective_space_' + name + '.png')

def plot_landuse_configuration(landuse, objectives, regionName):
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
    landuse_max_yield = landuse[np.argmax(-objectives[:,0], axis=0)]
    landuse_min_waterfootprint = landuse[np.argmax(objectives[:,1], axis=0)]
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

def plot_config_alternative_colors(landuse, objectives, regionName):
    
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
    landuse_max_yield = landuse[np.argmax(-objectives[:,0], axis=0)]
    landuse_min_waterfootprint = landuse[np.argmax(objectives[:,1], axis=0)]
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


def objectives_per_generation(res, regionName, unit_wf):
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
    ax3a.set_title(regionName + ': Objectives over generation', fontsize=10)
    ax3a.plot(n_gen, -np.array(obj_1))
    ax3a.set_xlabel("Generation")
    ax3a.set_ylabel("Maximum total yield [tonnes]")
    ax3b.plot(n_gen, np.array(obj_2))
    ax3b.set_xlabel("Generation")
    ax3b.set_ylabel("Water footprint " + unit_wf)
    plt.savefig(settings.get_default_directory() + "/objectives_over_generations_" + regionName)
    plt.show()

    # add here the generations you want to see in the plot
    #generations2plot = [10,20,30,40,50]
    generations2plot = [50,100,200,300,400,500]

    # make the plot
    fig4, ax4 = plt.subplots(1)
    # i - 1, because generation 1 has index 0
    for i in generations2plot:
        plt.scatter(-f[i-1][:,0],f[i-1][:,1])
    ax4.set_title(regionName + ': Parteto front for generations', fontsize=10)
    ax4.set_xlabel('Total yield [tonnes]')
    ax4.set_ylabel('Water footprint ' + unit_wf)
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
    ax5.set_title(regionName + ': Hypervolume for genrations', fontsize=10)
    ax5.plot(n_gen, hv, '-o', markersize=4, linewidth=2)
    ax5.set_xlabel("Generation")
    ax5.set_ylabel("Hypervolume")
    plt.savefig(settings.get_default_directory() + "/hypervolume_" + regionName + ".png")
    plt.show()

baseAmazonLanduse =  np.load(settings.get_file_reclass_amazon_npy())
baseCerradoLanduse = np.load(settings.get_file_reclass_cerrado_npy())

amazon_landuse = np.load(settings.get_file_amazon_landuse_results_500gen())
cerrado_landuse = np.load(settings.get_file_cerrado_landuse_results_500gen())

amazon_objectives = np.load(settings.get_file_amazon_objectives_results_500gen())
cerrado_objectives = np.load(settings.get_file_cerrado_objectives_results_500gen())

soyYieldAmazon = amazon_landuse[np.argmax(-amazon_objectives[:,0], axis=0)]
waterfootprintAmazon  = amazon_landuse[np.argmax(amazon_objectives[:,1], axis=0)]
soyYieldCerrado = cerrado_landuse[np.argmax(-cerrado_objectives[:,0], axis=0)]
waterfootprintCerrado = cerrado_landuse[np.argmax(cerrado_objectives[:,1], axis=0)]

print_land_use_change(compare_land_use(baseAmazonLanduse, soyYieldAmazon), "Amazon: Land use change\nmaximized total soy yield")
print_land_use_change(compare_land_use(baseAmazonLanduse, waterfootprintAmazon), "Amazon: Land use change\nminimized water footprint")
print_land_use_change(compare_land_use(baseCerradoLanduse, soyYieldCerrado), "Cerrado: Land use change\nmaximized total soy yield")
print_land_use_change(compare_land_use(baseCerradoLanduse, waterfootprintCerrado), "Cerrado: Land use change\nminimized water footprint")

plot_design_objective_space(amazon_landuse, amazon_objectives, "Amazon", "[Tonnes]")
plot_design_objective_space(cerrado_landuse, cerrado_objectives, "Cerrado", "[Tonnes]")

plot_landuse_configuration(amazon_landuse, amazon_objectives, "Amazon")
plot_landuse_configuration(cerrado_landuse, cerrado_objectives, "cerrado")

plot_config_alternative_colors(amazon_landuse, amazon_objectives, "Amazon")
plot_config_alternative_colors(cerrado_landuse, cerrado_objectives, "cerrado")

#objectives_per_generation(res_amazon, "Amazon", "[Tonnes]")
#objectives_per_generation(res_cerrado, "Cerrado", "[Tonnes]")

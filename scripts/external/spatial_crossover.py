import numpy as np
import random
from external import compute_genome
from pymoo.model.crossover import Crossover

class SpatialOnePointCrossover(Crossover):

    def __init__(self,n_points, **kwargs):
        super().__init__(2, 2, 1.0) # (n_parents,n_offsprings,probability) 
        self.n_points = n_points
    
    def _do(self, problem, X, **kwargs):
        _, n_matings= X.shape[0],X.shape[1]
        do_crossover = np.full(X[0].shape, True)
    
        # save dimensions of landuse maps
        shape_landusemaps = [X[0][_].shape[0],X[0][_].shape[1]]
        
        # child land use maps
        child_landuse_maps1 = []
        child_landuse_maps2 = []

        for _ in range(n_matings):

            # create patch map and genome with CoMOLA functions 
            patches_parent1, genome_parent1 = compute_genome.create_patch_ID_map(X[0][_],0,[3,4],"False")
            patches_parent2, genome_parent2 = compute_genome.create_patch_ID_map(X[1][_],0,[3,4],"False")
                        
            # define number of cuts
            num_crossover_points = self.n_points
            num_cuts = min(len(genome_parent1)-1, num_crossover_points)
            
            # select random places to cut genome
            cut_points = random.sample(range(1,min(len(genome_parent1),len(genome_parent2))), num_cuts)
            cut_points.sort()
            
            # define initial genome of children
            genome_child1 = list(genome_parent1)
            genome_child2 = list(genome_parent2)

            # get parts of genome from parents to children
            j=0
            for i in range(0,min(len(genome_parent1),len(genome_parent2))):
                if j < len(cut_points):
                    if i >= cut_points[j]: 
                        j=j+1
                # alternating parent 1 and 0
                if (j % 2) != 0: 
                    genome_child1[i] = 0.
                # alternating 0 and parent 2
                if (j % 2) == 0:
                    genome_child2[i] = 0.
            
            rows = shape_landusemaps[0]
            cols = shape_landusemaps[1]

            # fill in genome in patches
            child1 = patches_parent1
            child2 = patches_parent2

            for x in range(0, cols):
                for y in range(0, rows):
                    if child1[x, y] != 0:
                        child1[x, y] = genome_child1[child1[x, y] - 1]
                        child2[x, y] = genome_child2[child2[x, y] - 1]

            child1 = np.where(child1 == 0, X[1][_], child1)
            child2 = np.where(child2 == 0, X[0][_], child2)
            child_landuse_maps1.append(child1)
            child_landuse_maps2.append(child2)

        return np.array([np.array(child_landuse_maps1),np.array(child_landuse_maps2)])
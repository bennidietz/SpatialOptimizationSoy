import numpy as np
from pymoo.model.mutation import Mutation
from external import compute_genome

# function to randomly change a certain patch
def random_reset_mutation(genome_in, point_mutation_prob):
    genome = list(genome_in)
    for i in range(1, len(genome)):
        if np.random.uniform(0, 1) < point_mutation_prob:
            genome[i] = np.random.randint(low=1,high=3) 
    return (genome)


# class that performs the mutation
class SpatialNPointMutation(Mutation):
    def __init__(self, prob=None,point_mutation_probability=0.01):
        super().__init__()
        self.prob = prob
        self.point_mutation_probability = point_mutation_probability

    def _do(self, problem, X, **kwargs):
        shape_landusemaps = [X[0].shape[0], X[0].shape[1]]
        rows = shape_landusemaps[0]
        cols = shape_landusemaps[1]
        offspring = []

        for i in X:
            if np.random.uniform(0, 1) < self.prob:
                # leave out water water & urban area for optimization
                patches, genome = compute_genome.create_patch_ID_map(i, 0, [3,4], "False") 
                mutated_genome = random_reset_mutation(genome,
                                self.point_mutation_probability)

                # go back to land use map
                mutated_individual = patches
                for x in range(0, cols):
                    for y in range(0, rows):
                        if mutated_individual[x, y] != 0:
                            mutated_individual[x, y] = \
                                mutated_genome[mutated_individual[x, y] - 1]
                        else:
                            mutated_individual[x, y] = i[x,y]
                mutated_individual = np.where(mutated_individual == 0, i, mutated_individual)
                offspring.append(mutated_individual)
            
            # if no mutation
            else: 
                offspring.append(i)
        offspring = np.array(offspring) 
        return offspring
import numpy as np
from pymoo.model.sampling import Sampling
import initial_population, settings

class SpatialSampling(Sampling):
    def __init__(self, var_type=np.float,landuseData=None) -> None:
        super().__init__()
        self.var_type = var_type
        self.landuseData = landuseData
    def _do(self, problem, n_samples, **kwargs):
        settings.blockPrint()
        landusemaps_np = initial_population.initialize_spatial(n_samples,self.landuseData) # perform the actual initialization of the population
        settings.enablePrint()
        return landusemaps_np
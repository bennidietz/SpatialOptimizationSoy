import numpy as np

def getOccurancies(np_array):
    unique, counts = np.unique(np_array, return_counts=True)
    return dict(zip(unique, counts))
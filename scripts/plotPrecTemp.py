import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib.cm as cm
import numpy as np
import settings

temp_amazon = np.load(settings.get_file_temp_amazon())
temp_cerrado = np.load(settings.get_file_temp_cerrado())
prec_amazon = np.load(settings.get_file_prec_amazon())
prec_cerrado = np.load(settings.get_file_prec_cerrado())

temp_inter_amazon = np.load(settings.get_file_temp_amazon_interpolated())
temp_inter_cerrado = np.load(settings.get_file_temp_cerrado_interpolated())
prec_inter_amazon = np.load(settings.get_file_prec_amazon_interpolated())
prec_inter_cerrado = np.load(settings.get_file_prec_cerrado_interpolated())

plt.figure()

#subplot(r,c) provide the no. of rows and columns
f, axarr = plt.subplots(1,2) 

n_cells = 400
grid_x, grid_y = np.mgrid[0:n_cells, 0:n_cells]

def func(x, y):
    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

cmap_prec = clr.LinearSegmentedColormap.from_list('custom blue',['#3A6BE8','#1851AD'], N=10)
cmap_temp = clr.LinearSegmentedColormap.from_list('custom red',['#E93A3A','#AD1818'], N=10)

def visualizeData(np_array, np_array_interpolated, cmap):
    normalize = clr.Normalize(vmin=np_array.min(), vmax=np_array.max())
    scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=cmap)
    scalarmappaple.set_array(np_array)
    axarr[0].imshow(np_array, extent=(0,len(np_array),0,len(np_array)), origin='lower', cmap=cmap)
    axarr[1].imshow(np_array_interpolated, extent=(0,len(np_array_interpolated),0,len(np_array_interpolated)), origin='lower', cmap=cmap)
    plt.colorbar(scalarmappaple)
    plt.show()

visualizeData(prec_amazon, prec_inter_amazon, cmap_prec)
#visualizeData(prec_cerrado, prec_inter_cerrado, cmap_prec)
#visualizeData(temp_amazon, temp_inter_amazon, cmap_temp)
#visualizeData(temp_cerrado, temp_inter_cerrado, cmap_temp)
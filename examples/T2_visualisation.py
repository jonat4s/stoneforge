# %%

import numpy as np
import numpy.typing as npt
import pandas as pd
import lasio as las
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from stoneforge import preprocessing
from stoneforge.petrophysics import shale_volume
from stoneforge.petrophysics import water_saturation
from stoneforge.petrophysics import permeability
# %%

prj = preprocessing.project("C:\\Users\\jonatas\\Downloads\\nova_pasta")
prj.import_folder()
prj.well_names_paths


#%%
prj.import_well('3-BRSA-1053-RJS_NMR_SLB_merge')

data = prj.well_data

t2_dist = "T2_DIST" 

T2M = []
for mnm in data['3-BRSA-1053-RJS_NMR_SLB_merge']:
    if not mnm.find(t2_dist):
        print(mnm)
        T2 = data['3-BRSA-1053-RJS_NMR_SLB_merge'][mnm]['data']
        T2M.append(T2)

T2M = np.array(T2M).T
FF = data['3-BRSA-1053-RJS_NMR_SLB_merge']["CMFF"]['data']
print(FF)
print(np.shape(T2M))

plt.imshow(T2M)
plt.show()
# %%

T2DIST_KDE = []
for i in range(len(T2M)):
    #kde = gaussian_kde(T2M[i], bw_method = 0.1)

    kde = gaussian_kde(T2M[i], bw_method = 0.1)
    x = np.linspace(min(T2M[i])-0.005, max(T2M[i])+0.005, 1000)

    #print(x)
    #print(y)
    

    #x = np.linspace(min(T2M[i]), max(T2M[i]), 1000)  # Adjust the number of points as needed
    kde_values = kde(x)
    T2DIST_KDE.append(kde_values)
    #print(kde_values)

    # To visualize the KDE
    #plt.plot(x, kde_values)
    #plt.xlabel('X-axis')  # Replace with an appropriate label
    #plt.ylabel('KDE Values')  # Replace with an appropriate label
    #plt.show()
    #break

# %%

T2DIST_KDE = np.array(T2DIST_KDE)

#plt.imshow(T2DIST_KDE, cmap = 'jet',vmin = 0.51, vmax = 100)
plt.imshow(T2DIST_KDE, cmap = 'jet',vmin = 0.51, vmax = 100)
plt.colorbar()
plt.show()

# %%
T2DIST_KDE


# %%

rng = np.random.RandomState(42)
X = rng.random_sample((100, 3))
print(X)


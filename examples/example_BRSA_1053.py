# %%

import numpy as np
import numpy.typing as npt
import pandas as pd
import lasio as las
import matplotlib.pyplot as plt
from stoneforge import preprocessing
from scipy.stats import gaussian_kde
from stoneforge.petrophysics import shale_volume
from stoneforge.petrophysics import water_saturation
from stoneforge.petrophysics import permeability
# %%

prj = preprocessing.project("C:\\Users\\jonatas\\Downloads\\nova_pasta")
prj.import_folder()
prj.well_names_paths

# %%

prj.import_well('3-BRSA-1053-RJS_NMR_SLB_merge')

data = prj.well_data

for mnm in data['3-BRSA-1053-RJS_NMR_SLB_merge']:
    print(mnm)


# %%

print(data['3-BRSA-1053-RJS_NMR_SLB_merge']['MD']['data'])
print(data['3-BRSA-1053-RJS_NMR_SLB_merge']['MD']['unit'])

PHIT = data['3-BRSA-1053-RJS_NMR_SLB_merge']['TCMR']['data']
PHIE = data['3-BRSA-1053-RJS_NMR_SLB_merge']['CMRP_3MS']['data']
T2LM = data['3-BRSA-1053-RJS_NMR_SLB_merge']['T2LM']['data']
# %%

MD = data['3-BRSA-1053-RJS_NMR_SLB_merge']['MD']['data']
VSHALE = shale_volume.vshale('ehigie',phit = PHIT,phie = PHIE)
print(VSHALE)

# %%
FF = data['3-BRSA-1053-RJS_NMR_SLB_merge']['CMFF']['data']
SW = water_saturation.water_saturation( method = 'crain', phi = PHIE, ff = FF )
print(SW)

ln = len(PHIT)

#a1 = 1.
# %%
KSDR = data['3-BRSA-1053-RJS_NMR_SLB_merge']['KSDR']['data']
KTIM = data['3-BRSA-1053-RJS_NMR_SLB_merge']['KTIM']['data']
K_sdr = permeability.permeability(method = 'sdr', a1 = 1., phit = PHIT / 100 , m1 = 2, t2_lm = T2LM, n1 = 2)
K_tim = permeability.permeability(method = 'tim', a2 = 1., phit = PHIT / 100 , m2 = 2, bvm = FF, bvi = PHIT - PHIE, n2 = 2)

# %%

plt.plot(K_sdr, KSDR,'.')
plt.show()

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

#fig, ax = plt.subplots(1, 4, sharey =True)
fig, ax = plt.subplots(1, 4)
fig.set_size_inches(15, 12)

ax[0].plot(VSHALE, MD, color='green')
ax[0].set_title("VSHALE")
ax[0].set_xlabel("-")
ax[0].set_ylabel("DEPTH (m)")
ax[0].margins(y=0)
ax[0].invert_yaxis()
ax[0].grid()
ax[1].plot(SW, MD, color='blue')
ax[1].set_title("SW")
ax[1].set_xlabel("-")
ax[1].set_yticklabels([])
ax[1].margins(y=0)
ax[1].invert_yaxis()
ax[1].grid()
ax[2].plot(KTIM, MD, color='red', label = 'ktim')
ax[2].plot(KSDR, MD, color='teal', label = 'ksdr')
ax[2].set_xscale('log')
ax[2].set_title("Permeability(K)")
ax[2].set_xlabel("-")
ax[2].set_yticklabels([])
ax[2].margins(y=0)
ax[2].invert_yaxis()
ax[2].legend(loc = 0)
ax[2].grid()
ax[3]= plt.gca()
cax = ax[3].imshow(T2DIST_KDE, cmap = 'jet',vmin = 0.51, vmax = 100, extent= [0, 900, 0, len(MD) ])
ax[3].set_title('T2 Distribution')
ax[3].set_yticks([])
ax[3].set_xticks([])




# %%

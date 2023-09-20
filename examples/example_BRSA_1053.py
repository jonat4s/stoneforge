# %%

import numpy as np
import numpy.typing as npt
import pandas as pd
import lasio as las
import matplotlib.pyplot as plt
from stoneforge import preprocessing
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
K = permeability.permeability(method = 'sdr', a1 = 1., phit = PHIT / 100 , m1 = 2, t2_lm = T2LM, n1 = 2)
print(list(K))

# %%

plt.plot(K, KSDR,'.')
plt.show()

# %%

fig, ax = plt.subplots(1, 3)
fig.set_size_inches(12, 12)

ax[0].plot(VSHALE, MD, color='green')
ax[0].set_title("VSHALE")
ax[0].set_xlabel("-")
ax[0].set_ylabel("DEPTH (m)")
ax[0].invert_yaxis()
ax[0].grid()
ax[1].plot(SW, MD, color='blue')
ax[1].set_title("SW")
ax[1].set_xlabel("-")
ax[1].invert_yaxis()
ax[1].grid()
ax[2].plot(K, MD, color='blue')
ax[2].plot(KSDR, MD, color='teal')
ax[2].set_title("K")
ax[2].set_xlabel("-")
ax[2].invert_yaxis()
ax[2].grid()

# %%
plt.plot(K,'.')
plt.grid()
plt.show()
# %%

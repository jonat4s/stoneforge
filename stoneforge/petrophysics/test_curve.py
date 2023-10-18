#%%
import matplotlib as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
import lasio as las
import matplotlib.pyplot as plt
from stoneforge import preprocessing
from stoneforge.petrophysics import shale_volume
from stoneforge.petrophysics import water_saturation
from stoneforge.petrophysics import permeability

prj = preprocessing.project("C:\\Users\\jonatas\\Downloads\\nova_pasta")
prj.import_folder()
prj.well_names_paths

#%%
prj.import_well('3-BRSA-1053-RJS_NMR_SLB_merge')

data = prj.well_data

for mnm in data['3-BRSA-1053-RJS_NMR_SLB_merge']:
    print(mnm)

T2 = data['3-BRSA-1053-RJS_NMR_SLB_merge']['data']

print(T2)

#%%
ax[0].plot(VSHALE, MD, color='green')
ax[0].set_title("VSHALE")
ax[0].set_xlabel("-")
ax[0].set_ylabel("DEPTH (m)")
ax[0].invert_yaxis()
ax[0].grid()
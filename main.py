import brian2 as b2

# b2.clear_cache('cython')

import matplotlib.pyplot as plt
import numpy as np
import random as ran
import os

from parameters import *
from equations import *
from groupsandsynapses import *
from test import *

ran.seed(42)

duration = 2000*b2.ms
deft = b2.defaultclock.dt
t_recorded = np.arange(int(duration/deft))*deft

b2.run(300*b2.ms)

variables_to_record = ['V']

'''
monitord1 = b2.StateMonitor(D1, variables=variables_to_record, record=True)
monitord2 = b2.StateMonitor(D2, variables=variables_to_record, record=True)
monitorfsn = b2.StateMonitor(FSN, variables=variables_to_record, record=True)
monitorstn = b2.StateMonitor(STN, variables=variables_to_record, record=True)
monitorgpti = b2.StateMonitor(GPTI, variables=variables_to_record, record=True)
monitorgpta = b2.StateMonitor(GPTA, variables=variables_to_record, record=True)
monitorgpi = b2.StateMonitor(GPI, variables=variables_to_record, record=True)
'''

spikesd1 = b2.SpikeMonitor(D1)
spikesd2 = b2.SpikeMonitor(D2)
spikesfsn = b2.SpikeMonitor(FSN)
spikesstn = b2.SpikeMonitor(STN)
spikesgpti = b2.SpikeMonitor(GPTI)
spikesgpta = b2.SpikeMonitor(GPTA)
spikesgpi = b2.SpikeMonitor(GPI)

spikemonitors = [spikesd1, spikesd2, spikesfsn, spikesgpi, spikesgpta, spikesgpti, spikesstn]
nuclei = ['D1', 'D2', 'FSN','GPi', 'GPeTA', 'GPeTI', 'STN']

firingratesd1 = []
firingratesd2 = []
firingratesfsn = []
firingratesgpi = []
firingratesgpta = []
firingratesgpti = []
firingratesstn = []

b2.store()

c_var1 = np.arange(0., 0.1, 0.01)
c_var2 = np.arange(0.1, 1.1, 0.1)
c_var = np.concatenate((c_var1,c_var2))

# file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'frandff.txt')
file_path = '/home/f_mastellone/frandff.txt'
text_file = open(file_path, "w")

for i, c_i in enumerate(c_var):
    b2.restore()
    c = c_i
    b2.run(duration)

    text_file.write(f"Correlation parameter: {c}\n")

    print(f"Correlation parameter: {c}\n")

    text_file.write(f'Firing rate D1: {np.mean(spikesd1.count/duration)} spikes/second\n')
    firingratesd1.append(np.mean(spikesd1.count/duration))
    text_file.write(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second\n')
    firingratesd2.append(np.mean(spikesd2.count/duration))
    text_file.write(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')
    firingratesfsn.append(np.mean(spikesfsn.count/duration))

    print(f'Firing rate D1: {np.mean(spikesd1.count/duration)} spikes/second')
    print(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second')
    print(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')

    text_file.write(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second\n')
    firingratesstn.append(np.mean(spikesstn.count/duration))
    text_file.write(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second\n')
    firingratesgpti.append(np.mean(spikesgpti.count/duration))
    text_file.write(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second\n')
    firingratesgpta.append(np.mean(spikesgpta.count/duration))
    text_file.write(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')
    firingratesgpi.append(np.mean(spikesgpi.count/duration))

    print(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second')
    print(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second')
    print(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second')
    print(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')
text_file.close()

###### Save Raster Plots
save_path = '/home/f_mastellone/rasterplots'
if not os.path.exists(save_path):
    os.makedirs(save_path)
for spkmon, nuclues in zip(spikemonitors, nuclei):
    rasterplot(spkmon, f'Raster Plot {nucleus}', save_path)

###### Save Plots of Firing Rates against Correlation parameters
froverc = [firingratesd1, firingratesd2, firingratesfsn, firingratesgpi, firingratesgpta, firingratesgpti, firingratesstn]
save_path = '/home/f_mastellone/fragainstc'
if not os.path.exists(save_path):
    os.makedirs(save_path)

for firingrate, nucleus in zip(froverc, nuclei):
    plt.figure(frvc)
    plt.title(f'FR against c for {nucleus}')
    plt.plot(c_var, firingrate)
    plt.xlabel('c')
    plt.ylabel('Firing Rate [spikes/second]')
    plt.savefig(save_path, bbox_inches='tight')
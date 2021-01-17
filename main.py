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

variables_to_record = ['V']

nuclei = ['D1', 'D2', 'FSN','GPi', 'GPeTA', 'GPeTI', 'STN']
firingratesd1 = []
firingratesd2 = []
firingratesfsn = []
firingratesgpi = []
firingratesgpta = []
firingratesgpti = []
firingratesstn = []

# file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'frandff.txt')
file_path = '/home/f_mastellone/frandff.txt'
text_file = open(file_path, "w")

net = b2.Network(b2.collect())
net.store()

c_var = np.arange(0., 0.11, 0.01)
for i, c_i in enumerate(c_var):
    net.restore()
    c = c_i

    net.run(300*b2.ms)

    spikesd1 = b2.SpikeMonitor(D1)
    spikesd2 = b2.SpikeMonitor(D2)
    spikesfsn = b2.SpikeMonitor(FSN)
    spikesstn = b2.SpikeMonitor(STN)
    spikesgpti = b2.SpikeMonitor(GPTI)
    spikesgpta = b2.SpikeMonitor(GPTA)
    spikesgpi = b2.SpikeMonitor(GPI)

    spikemonitors = [spikesd1, spikesd2, spikesfsn, spikesgpi, spikesgpta, spikesgpti, spikesstn]

    net.run(duration)

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

    ###### Save Raster Plots
    save_path = '/home/f_mastellone/rasterplots'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for spkmon, nucleus in zip(spikemonitors, nuclei):
        save_path_f = os.path.join(save_path, f'{nucleus}c{c}.png')
        rasterplot(spkmon, f'Raster Plot {nucleus} c:{c}', save_path_f)

text_file.close()

###### Save Plots of Firing Rates against Correlation parameters
froverc = [firingratesd1, firingratesd2, firingratesfsn, firingratesgpi, firingratesgpta, firingratesgpti, firingratesstn]
save_path = '/home/f_mastellone/fragainstc'
if not os.path.exists(save_path):
    os.makedirs(save_path)

for firingrate, nucleus in zip(froverc, nuclei):
    save_path_f = os.path.join(save_path, f'frc{nucleus}.png')
    plt.figure()
    plt.title(f'FR against c for {nucleus}')
    plt.plot(c_var, firingrate, '.-')
    plt.xlabel('c')
    plt.ylabel('Firing Rate [spikes/second]')
    plt.savefig(save_path_f, bbox_inches='tight')
    plt.close()

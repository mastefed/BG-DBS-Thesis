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

monitord1 = b2.StateMonitor(D1, variables=['V'], record=True)
spikesd1 = b2.SpikeMonitor(D1)

monitord2 = b2.StateMonitor(D2, variables=['V'], record=True)
spikesd2 = b2.SpikeMonitor(D2)

monitorfsn = b2.StateMonitor(FSN, variables=['V'], record=True)
spikesfsn = b2.SpikeMonitor(FSN)

monitorstn = b2.StateMonitor(STN, variables=['V'], record=True)
spikesstn = b2.SpikeMonitor(STN)

monitorgpti = b2.StateMonitor(GPTI, variables=['V'], record=True)
spikesgpti = b2.SpikeMonitor(GPTI)

monitorgpta = b2.StateMonitor(GPTA, variables=['V'], record=True)
spikesgpta = b2.SpikeMonitor(GPTA)

monitorgpi = b2.StateMonitor(GPI, variables=['V'], record=True)
spikesgpi = b2.SpikeMonitor(GPI)

c_var = [0.]

save_to_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'output.txt')
text_file = open(save_to_file, "w")

for i, c_i in enumerate(c_var):
    c = c_i
    b2.run(duration)

    text_file.write(f"Correlation parameter: {c}\n")

    text_file.write(f'Firing rate D1: {np.mean(spikesd1.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')

    text_file.write(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')

    ff_fsn = fanofactor(duration, spikesfsn, neuron['FSN'], 0*b2.ms, 2*b2.ms, 2*b2.ms)
    ff_d1 = fanofactor(duration, spikesd1, neuron['D1'], 0*b2.ms, 2*b2.ms, 2*b2.ms)
    ff_d2 = fanofactor(duration, spikesd2, neuron['D2'], 0*b2.ms, 2*b2.ms, 2*b2.ms)

    text_file.write(f"FF FSN: {ff_fsn}\n")
    text_file.write(f"FF D1: {ff_d1}\n")
    text_file.write(f"FF D2: {ff_d2}\n")

    """plt.figure(i)
    plt.subplot(3,1,1)
    plt.title(f"Raster Plot c={c}")
    plt.plot(spikesd1.t/b2.ms, spikesd1.i, 'o', ms=0.5, label='D1')
    plt.ylabel('indices')
    plt.xlim((0.+i*2000.,2000.+i*2000.))
    plt.legend()

    plt.subplot(3,1,2)
    plt.plot(spikesd2.t/b2.ms, spikesd2.i, 'o', ms=0.5, label='D2')
    plt.ylabel('indices')
    plt.xlim((0.+i*2000.,2000.+i*2000.))
    plt.legend()

    plt.subplot(3,1,3)
    plt.plot(spikesfsn.t/b2.ms, spikesfsn.i, 'o', ms=0.5, label='FSN')
    plt.xlabel('time [ms]')
    plt.ylabel('indices')
    plt.xlim((0.+i*2000.,2000.+i*2000.))
    plt.legend()"""

# plt.show()
text_file.close()
import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
import random as ran

from parameters import *
from equations import *
from groupsandsynapses import *

ran.seed(42)

duration = 1000*b2.ms
deft = b2.defaultclock.dt
t_recorded = np.arange(int(duration/deft))*deft

b2.run(300*b2.ms)

monitord1 = b2.StateMonitor(D1, variables=['V'], record=True)
spikesd1 = b2.SpikeMonitor(D1, variables=['V'])

monitord2 = b2.StateMonitor(D2, variables=['V'], record=True)
spikesd2 = b2.SpikeMonitor(D2, variables=['V'])

monitorfsn = b2.StateMonitor(FSN, variables=['V'], record=True)
spikesfsn = b2.SpikeMonitor(FSN, variables=['V'])

monitorstn = b2.StateMonitor(STN, variables=['V'], record=True)
spikesstn = b2.SpikeMonitor(STN, variables=['V'])

monitorgpti = b2.StateMonitor(GPTI, variables=['V'], record=True)
spikesgpti = b2.SpikeMonitor(GPTI, variables=['V'])

monitorgpta = b2.StateMonitor(GPTA, variables=['V'], record=True)
spikesgpta = b2.SpikeMonitor(GPTA, variables=['V'])

monitorgpi = b2.StateMonitor(GPI, variables=['V'], record=True)
spikesgpi = b2.SpikeMonitor(GPI, variables=['V'])

b2.run(duration)

print(f"Correlation parameter: {c}")

print(f'\nFiring rate D1: {np.mean(spikesd1.count/duration)} spikes/second\n')
print(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second\n')
print(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')

print(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second\n')
print(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second\n')
print(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second\n')
print(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')